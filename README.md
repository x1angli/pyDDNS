DDNS-chiasma
============

A Dynamic DNS system that updates DNS records 

# Introduction
This python file has three modules: 
* Server
* Upstream
* Downstream

`Server` provide Restful Api to get client IP, get silo list and maintain each silo

`Client/Upstream` can check public IP of local host, then update dns recoder of silo specified in `Client/config.yml`

`Client/Downstream` can get dns recoder of silo specified in `Client/config.yml`, then modify local `host file` to change DNS rules.

## How does it work
### On the upstream machine
1. Request `Get /ip` to check current public IP.
2. Request `Get /silos/silo_id` to check if the ip address of dnsrecords has changed.
3. If changed, Request `PUT /silos/silo_id` to update dnsrecords.

### On the downstream machine
1. Request `Get /silos/silo_id` to get dnsrecords.
2. Change host file with dnsrecords.

### On the server
Server uses web framework flask to build REST API.

## Installation
1. Make sure Python is properly installed on all platforms (i.e. Server, Upstream, Downstream)
2. Modify the `/server/config.yml` file to change DB setting, and `/client/config.yml` file to specify Server and DNS details
3. Execute following commands

        pip install -r requirements.txt
        flask --app=server.app initdb


## Start using the server
1. Execute following commands
 
        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python server/app.py
        
2. Open your browser, visit `http://localhost:81/ping`, and you would get the ping-pong JSON.
3. Alternatively, use `curl` to get it:

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
        
#### Notice
The command above is executed in Windows environment.But in Linux environment, the command, reference and separator for environment variable to set PYTHONPATH are different.

1. Windows
use `set` command
use `% %` to reference the environment variable
use `;` as the separator

        set PYTHONPATH=%PYTHONPATH%;.
        
2. Linux
use `export` command
use `$` to reference the environment variable
use `:` as the separator

        export PYTHONPATH=$PYTHONPATH:.
        
Please use the correct command to set PYTHONPATH according to your system environment.

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
        
### ping()
A simple ping request to let you know things are working.

1. Request
        
        GET /ping

2. Parameters
        
        None

3. JSON Result
        
        {"message": "PONG"}

4. Curl Example
        
        curl -X GET http://localhost:5000/ping

### getip()
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

### listsilos(user)
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

### getsilo(silo_id, user)
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

### putsilo(silo_id, user)
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