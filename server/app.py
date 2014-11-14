import json
from flask import Flask, request, abort, make_response, Response
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps

from server.models import *


app = Flask(__name__)
app.config.update(svrcfg['flask'])

def loadData():
    pass


def authenticate(role=None):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth:
                abort(401, description='You must provide authentication information')
            try:
                user = session.query(User).filter(User.id == auth.username).one()
            except NoResultFound:
                abort(401, description='The user {} does nott exist!'.format(auth.username))
            if user.password != auth.password:
                abort(401, description='Password of user {} is incorrect!'.format(auth.username))
            if role is not None and user.role != role:
                abort(401, description='Unauthorized Access')
            return func(*args, user=user, **kwargs)
        return decorated
    return wrapper


def errorjson(error, status):
    responseobj = {'message': error.description, 'http_code': status}
    return Response(to_json(responseobj), status=status, mimetype='application/json')


@app.errorhandler(400)
def badrequest(error):
    return errorjson(error, 400)


@app.errorhandler(401)
def unauthenticated(error):
    return make_response(error.description, 401, {'WWW-Authenticate': 'Basic realm="flask-chiasma"'})

@app.errorhandler(403)
def badrequest(error):
    return errorjson(error, 403)


def to_json(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    if isinstance(obj, list):
        return '[\r\n' + '.\r\n'.join(elem.to_json() for elem in obj) + '\r\n]'
    else:
        return json.dumps(obj)

def jsonresp(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        respobj = func(*args, **kwargs)
        return Response(to_json(respobj), status=200, mimetype='application/json')
    return decorated



@app.cli.command('initdb')
def initdb_command():
    print('Initializing the database...')
    print('Creating tables...')
    init_schema()

    print('All tables created. Populating all data...')
    user1 = User('cumuli', 'cumuli123', 'admin')
    user2 = User('normal', 'normal123', 'common')
    session.add(user1)
    session.add(user2)
    session.commit()

    silo1 = Silo('silo1', 'cumuli')
    silo2 = Silo('silo2', 'normal')
    session.add(silo1)
    session.add(silo2)
    session.commit()

    webserver = DnsRecord('silo1', 'webserver', '127.0.0.1')
    dbserver = DnsRecord('silo1', 'dbserver', '127.0.0.1')
    session.add(webserver)
    session.add(dbserver)
    webserver2 = DnsRecord('silo2', 'webserver', '127.0.0.1')
    dbserver2 = DnsRecord('silo2', 'dbserver', '127.0.0.1')
    session.add(webserver2)
    session.add(dbserver2)
    session.commit()

    print('Initialized the database.')

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.route('/', methods=['GET'])
@jsonresp
def getindex():
    return {'message': 'Please refer to our api'}


@app.route('/ping', methods=['GET', 'POST', 'PUT'])
@jsonresp
def ping():
    return {'message': 'PONG'}


@app.route('/ip', methods=['GET'])
@jsonresp
def getip():
    """
    Echos client's IP address
    """
    # request.META['REMOTE_ADDR']
    return {'ip': request.remote_addr}


@app.route('/silos', methods=['GET'])
@jsonresp
@authenticate('admin')
def listsilos(user):
    result = session.query(Silo).all()
    return result


@app.route('/silos/<string:silo_id>', methods=['GET'])
@jsonresp
@authenticate()
def getsilo(silo_id, user):
    try:
        silo = session.query(Silo).filter(Silo.id==silo_id).one()
    except NoResultFound:
        abort(404, '%s not found' % silo_id)
    if silo.user_id != user.id:
        abort(401, description='You do not have the access to the silo')
    return silo

@app.route('/silos/<string:silo_id>', methods=['PUT'])
@jsonresp
@authenticate()
def putsilo(silo_id, user):
    try:
        silo = session.query(Silo).filter(Silo.id==silo_id).one()
    except NoResultFound:
        abort(404, "%s not found" % silo_id)
    if silo.user_id != user.id:
        abort(401, description='You do not have the access to the silo')
    try:
        reqjson = request.get_json(force=True, silent=True)
        if not reqjson:
            abort(400, 'The request must be a valid json')
        if not 'id' in reqjson:
            abort(400, 'The request body json must contain a valid "ip" field')
        if silo_id != reqjson['id']:
            abort(403, 'The silo\'s id in request must match the one in URL. "%s" v.s. "%s"' % (silo_id, reqjson['id']) )
        if not 'dnsrecords' in reqjson:
            abort(400, 'The request body json must contain a valid "dnsrecords" field')
        dns_records = reqjson['dnsrecords']
        for dns_record in dns_records:
            if not 'hostname' in dns_record:
                 abort(400, 'The dnsrecord "%s" must have a valid "hostname" key' % dns_record)
            if not 'ip' in dns_record:
                 abort(400, 'The dnsrecord "%s" must have a valid "ip" key' % dns_record)

        session.query(DnsRecord).filter(DnsRecord.silo_id==silo_id).delete()
        session.query(Silo).filter(Silo.id==silo_id).delete()

        silo = Silo(silo_id)
        session.add(silo)

        for dns_record in dns_records:
            dnsrecord = DnsRecord(silo_id, dns_record['hostname'], dns_record['ip'])
            session.add(dnsrecord)

        session.commit()
        return session.query(Silo).filter(Silo.id==silo_id).one()
    except:
        session.rollback()
        raise

@app.route('/silos/<string:silo_id>', methods=['DELETE'])
@jsonresp
@authenticate('admin')
def deletesilo(silo_id, user):
    try:
        silo = session.query(Silo).filter(Silo.id==silo_id).one()
    except NoResultFound:
        abort(404, "%s not found" % silo_id)
    if silo.user_id != user.id:
        abort(401, description='You do not have the access to the silo')
    try:
        session.query(DnsRecord).filter(DnsRecord.silo_id==silo_id).delete()
        session.query(Silo).filter(Silo.id==silo_id).delete()
    except:
        session.rollback()
        raise


if __name__ == '__main__':
    loadData()
    print("Running web service... Press CTRL-C to terminate")
    app.run()
