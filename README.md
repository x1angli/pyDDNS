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

# Installation
1. Make sure Python is properly installed on all platforms (i.e. Server, Upstream, Downstream)
1. Modify the `/server/config.yml` file to change DB setting, and `/client/config.yml` file to specify Server and DNS details
1. Execute following commands

        pip install -r requirements.txt
        flask --app=server.app initdb


# Start using the server
1. Execute following commands
 
        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python server/app.py
        
1. Open your browser, visit `http://localhost:81/ping`, and you would get the ping-pong JSON.
1. Alternatively, use `curl` to get it:

        curl -X GET http://localhost:81/ping
    
For other curl examples, see https://public-api.sonic.net/dyndns

# Start using the client
1. On the downstream machine, execute following commands
 
        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python client/downstream.py

2. On the upstream machine, execute following commands
 
        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python client/upstream.py
        
# Rest Api introduction
## *Ping the server

A simple ping request to let you know things are working.
### Request
GET /ping
### Parameters
None
### JSON Result
    {"message": "PONG"}
### Curl Example
    curl -X GET http://localhost:5000/ping
    
## *Getting your ip address

This allows you to get your current public ip address.   
Note this may not work correctly if you are behind a proxy.
### Request
GET /ip
### Parameters
None
### JSON Result
    {"ip": "127.0.0.1"}
### Curl Example
    curl -X GET http://localhost:5000/ip
    
## *Get silos list

unfinished

## *Get silo

unfinished
    
## *Update silo

unfinished

## *delete silo

unfinished


# How does it work
1. On the upstream machine

2. On the downstream machine        

3. On the downstream machine

