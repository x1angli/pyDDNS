DDNS-chiasma
============

A Dynamic DNS system that updates DNS records 

# Introduction
This Python project has three modules: 

1. Server

`Server` provide Restful API to get client IP, get silo list and maintain each silo.

2. Upstream

`Client/Upstream` can check public IP of local host, then update dns recoder of silo specified in `Client/config.yml`

3. Downstream

`Client/Downstream` can get dns recoder of silo specified in `Client/config.yml`, then modify local `host file` to change DNS rules.


## How does it work
1. On the upstream machine

1. On the downstream machine    

1. On the server


## Installation
1. Make sure Python is properly installed on all platforms (i.e. Server, Upstream, Downstream)
1. Modify the `/server/config.yml` file to change DB setting, and `/client/config.yml` file to specify Server and DNS details
1. Execute following commands

    pip install -r requirements.txt
    flask --app=server.app initdb


## Start using the server
1. Execute following commands
 
    cd DDNS-chiasma
    set PYTHONPATH=%PYTHONPATH%;.
    python server/app.py
    
1. Open your browser, visit `http://localhost:81/ping`, and you would get the ping-pong JSON.
1. Alternatively, use `curl` to get it:

    curl -X GET http://localhost:81/ping
    
## Start using the client
### Downstream (End user)
On the downstream machine, execute following commands
 
    cd DDNS-chiasma
    set PYTHONPATH=%PYTHONPATH%;.
    python client/downstream.py

### Upstream (The endpoint with dynamic IP)
On the upstream machine, execute following commands
 
    cd DDNS-chiasma
    set PYTHONPATH=%PYTHONPATH%;.
    python client/upstream.py
    
## RESTful API Specification
### getindex()

1. Request

    GET /
    
2. Parameters

    None
    
3. JSON Result

    {'message': 'Please refer to our api'}
    
4. Curl Example

    curl -X GET http://localhost:5000/
    
### ping
A simple ping request to let you know things are working.

1. Request
    
    GET /ping

2. Parameters
    
    None

3. JSON Result
    
    {"message": "PONG"}

4. Curl Example
    
    curl -X GET http://localhost:5000/ping

### getip
This allows you to get your current public ip address.   
Note this may not work correctly if you are behind a proxy.

1. Request

    GET /ip
    
2. Parameters

    None
    
3. JSON Result

    {"ip": "127.0.0.1"}
    
4. Curl Example

    curl -X GET http://localhost:5000/ip

### listsilos
For each silo that include dnsrecorder. Even dnsrecorder in different webservice.
 
1. Request

    GET /silos
    
2. Parameters

    None
    
3. JSON Result

    [
    {"id": "silo1", "dnsrecords": [
    {"hostname": "dbserver", "ip": "127.0.0.1"}, 
    {"hostname": "webserver", "ip": "127.0.0.1"}
    ]}.
    {"id": "silo2", "dnsrecords": [
    {"hostname": "dbserver", "ip": "127.0.0.1"}, 
    {"hostname": "webserver", "ip": "127.0.0.1"}
    ]}
    ]

4. Curl Example

    curl -X GET http://localhost:5000/silos

### getsilo
To get a silo by silo id.

1. Request

    GET /silos/silo_id
    
2. Parameters

    silo_id
    
3. JSON Result

    {"id": "silo1", "dnsrecords": [
    {"hostname": "dbserver", "ip": "127.0.0.1"}, 
    {"hostname": "webserver", "ip": "127.0.0.1"}
    ]}

4. Curl Example

    curl -X GET http://localhost:5000/silos/silo1

### putsilo
To update a silo by silo id.

1. Request

    PUT /silos/silo_id
    
2. Parameters

    silo_id
    
3. JSON Result

    {"id": "silo1", "dnsrecords": [
    {"hostname": "dbserver", "ip": "127.0.0.1"}, 
    {"hostname": "webserver", "ip": "127.0.0.1"}
    ]}

4. Curl Example

    curl -X PUT http://localhost:5000/silos/silo1
    
### deletesilo(silo_id, user)
To delete a silo by silo id.

1. Request

    DELETE /silos/silo_id
    
2. Parameters

    silo_id
    
3. JSON Result

    None
    
4. Curl Example

    curl -X DELETE http://localhost:5000/silos/silo1
