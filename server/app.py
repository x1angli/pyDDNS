import json
from flask import Flask, request, abort, make_response, Response
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.contrib.fixers import ProxyFix

from server.models import *


app = Flask(__name__)
app.config.update(svrcfg['flask'])

def loadData():
    pass


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            abort(401, description="You must provide authentication information")
        try:
            user = session.query(User).filter(User.id == auth.username).one()
        except NoResultFound as e:
            abort(401, description="User {} doesn't exist! ".format(auth.username))
        if user.password != auth.password:
            abort(401, description="Password of user {} is incorrect!".format(auth.username))
        return func(*args, **kwargs)
    return decorated


def authenticate_authorize(role):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth:
                abort(401, description="You must provide authentication information")
            try:
                user = session.query(User).filter(User.id == auth.username).one()
            except NoResultFound:
                abort(401, description="user {} doesn't exist! ".format(auth.username))
            if user.password != auth.password:
                abort(401, description="Password of user {} is incorrect!".format(auth.username))
            if user.role_id != role:
                abort(401, description="Unauthorized Access")
            return func(*args, **kwargs)
        return decorated
    return wrapper


def errorjson(error, status):
    responseobj = {"message": error.description, "http_code": status}
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
    roleadmin = Role('admin')
    rolecommon = Role('common')
    session.add(roleadmin)
    session.add(rolecommon)
    session.commit()

    user1 = User('admin', 'cumuli', 'cumuli123')
    session.add(user1)
    session.commit()

    silo1 = Silo('silo1')
    session.add(silo1)
    session.commit()

    webserver = DnsRecord('silo1', 'webserver', '127.0.0.1')
    dbserver = DnsRecord('silo1', 'dbserver', '127.0.0.1')
    session.add(webserver)
    session.add(dbserver)
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
@authenticate_authorize('admin')
def listsilos():
    result = session.query(Silo).all()
    return result


@app.route('/silos/<string:silo_id>', methods=['GET'])
@jsonresp
@authenticate_authorize('admin')
def getsilo(silo_id):
    result = session.query(Silo).filter(Silo.id==silo_id).one()
    # session.commit()
    return result

@app.route('/silos/<string:silo_id>', methods=['PUT'])
@jsonresp
@authenticate_authorize('admin')
def putsilo(silo_id):
    try:
        reqjson = request.get_json(force=True, silent=True)
        if not reqjson:
            abort(400, 'The request must be a valid json')
        if not 'id' in reqjson:
            abort(400, 'The request body json must contain a valid "ip" field')
        if (silo_id != reqjson['id']):
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
@authenticate_authorize('admin')
def deletesilo(silo_id):
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
