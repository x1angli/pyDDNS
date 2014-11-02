DDNS-chiasma
============

A Dynamic DNS system that updates DNS records 

# Introduction
This python file has three modules: 
* Server
* Upstream
* Downstream

# Installation
1. Make sure Python is properly installed on all platforms (i.e. Server, Upstream, Downstream)
1. Modify the `/server/config.yml` file
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
