__author__ = 'main'

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship

from sqlalchemy.ext.declarative import declarative_base

from server.config import svrcfg


engine = create_engine(svrcfg['SQLALCHEMY_DATABASE_URI'])

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
session = scoped_session(Session)

Base = declarative_base()



class User(Base):
    __tablename__ = 'user'

    role_id = Column(String(20), ForeignKey('role.id'))
    id = Column(String(20), primary_key=True)
    password = Column(String(20))

    def __init__(self, role_id, id, password):
        self.role_id = role_id
        self.id = id
        self.password = password

    def to_json(self):
        return '{"id": "%s", "type": "User"}' % (self.id)

    def __repr__(self):
        return "<User(id='%s')>" % (self.id)

class Role(Base):
    __tablename__ = 'role'

    id = Column(String(20), primary_key=True)
    user_id = relationship("User", backref=backref("role", lazy="joined"))

    def __init__(self, id):
        self.id = id

    def to_json(self):
        return '{"rolename": "%s"}' % self.id

    def __repr__(self):
        return self.to_json()

class Silo(Base):
    __tablename__ = 'silo'

    id = Column(String(20), primary_key=True)
    dnsrecords = relationship("DnsRecord", backref=backref("silo", lazy="joined")) # automatically populates the property

    def __init__(self, id):
        self.id = id

    def to_json(self):
        return '{"id": "%s", "dnsrecords": [\r\n%s\r\n]}' % (self.id, ', \r\n'.join([record.to_json() for record in self.dnsrecords]))

    def __repr__(self):
        return self.to_json()
         # return "<Silo (id='%s', dnsrecords='%s')>" % (self.id, self.dnsrecords)

class DnsRecord(Base):
    __tablename__ = 'dnsrecord'

    silo_id = Column(String(20), ForeignKey('silo.id'), primary_key=True)
    hostname = Column(String(20), primary_key=True)
    ip = Column(String(20))

    def __init__(self, silo_id, hostname, ip):
        self.silo_id = silo_id
        self.hostname = hostname
        self.ip = ip

    def to_json(self):
        return '{"hostname": "%s", "ip": "%s"}' % (self.hostname, self.ip)

    def __repr__(self):
        return self.to_json()
        # return "<DnsRecord(name='%s', value='%s')>" % (self.hostname, self.ip)


def clear_schema():
    Base.metadata.drop_all(engine)

def init_schema():
    Base.metadata.create_all(engine)

