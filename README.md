DDNS-chiasma
============

A Dynamic DNS system that updates DNS records 

# Introduction
This python file has three modules: 
* Server
* Upstream
* Downstream

`Server` provides Restful API to get client IP, get silo list and maintain each silo

`client/upstream` can check public IP of local host, then update dns recoder of silo specified in `client/config.yml`

`client/downstream` can get dns recoder of silo specified in `client/config.yml`, then modify local host file to change DNS rules.

## How does it work
### On the upstream machine
There is a file named `client/config.yml` to store Server and DNS details. `client/upstream` can checks current public IP, and sends `Get /silos/silo_id` request to check if the ip address of dns records has changed. If the ip address of dns records has changed, it will send `PUT /silos/silo_id` request to update dns recoder of silo specified in `client/config.yml`.

The setting file `client/config.yml` provides a entry named `getIpFrom`. Set to `Socket`, if your upstream machine has an independent public IP. Otherwise, setting to `ServerApi` may work in your situation.

### On the downstream machine
`client/downstream` sends `Get /silos/silo_id` request to get dns recoder of silo specified in `client/config.yml` mentioned above, and modify local host file to change DNS rules.

### On the server
`server` provide Restful API to get client IP, get silo list and maintain each silo. And there is also a file named `client/config.yml` to store DB settings like `username`, you can modify settings in the file for your actual situation. 

`server` uses web framework Flask to build RESTful API. For more details, please read the "RESTful API Specification" section.

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
On the upstream machine, execute following commands:

        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python client/upstream.py

#### Notice
The command above is executed in Windows environment.But in Linux environment, the command, reference and separator for environment variable to set PYTHONPATH are different.

**Windows**
* use `set` command
* use `% %` to reference the environment variable
* use `;` as the separator

        set PYTHONPATH=%PYTHONPATH%;.

**Linux**
* use `export` command
* use `$` to reference the environment variable
* use `:` as the separator

        export PYTHONPATH=$PYTHONPATH:.

Please use the correct command to set PYTHONPATH according to your system environment.

## How to run it automatically
If you want to run it automatically, please read this section and follow the instructions to set your computer settings.

### Task Scheduler in Windows
Task Scheduler enables you to automatically perform routine tasks on a chosen computer. Task Scheduler does this by monitoring whatever criteria you choose to initiate the tasks and then executing the tasks when the criteria is met.

1. Open Task Scheduler by clicking the **Start** button, clicking **Control Panel**, clicking **System and Security**, clicking **Administrative Tools**, and then double-clicking **Task Scheduler**. 
2. Click the **Action** menu, and then click **Create Basic Task**.
3. Type a name for the task and an optional description, and then click **Next**.
4. Do one of the following:
    * To select a schedule based on the calendar, click **Daily**, **Weekly**, **Monthly**, or **One time**, click **Next**; specify the schedule you want to use, and then click **Next**.
    * To select a schedule based on common recurring events, click **When the computer starts** or **When I log on**, and then click **Next**.
    * To select a schedule based on specific events, click **When a specific event is logged**, click **Next**; specify the event log and other information using the drop-down lists, and then click **Next**.
5. To schedule a program to start automatically, click **Start a program**, and then click **Next**.
6. Click **Browse** to find the program you want to start, and then click **Next**.
7. Click **Finish**.

For more details about Task Scheduler, please click [here](http://windows.microsoft.com/en-US/windows/schedule-task#1TC=windows-7).

### Cron job in Linux
Cron job are used to schedule commands to be executed periodically. You can setup commands or scripts, which will repeatedly run at a set time. Cron is one of the most useful tool in Linux. 

To edit your crontab file, type the following command at the UNIX / Linux shell prompt:

    $ crontab -e
    
The syntax is:

    1 2 3 4 5 /path/to/command
    
Where,
* 1: Minute (0-59)
* 2: Hours (0-23)
* 3: Day (0-31)
* 4: Month (0-12 [12 == December])
* 5: Day of the week(0-7 [7 or 0 == sunday])
* /path/to/command - Script or command name to schedule

operator allows you to specifying multiple values in a field. There are three operators:
* The asterisk (*) : This operator specifies all possible values for a field
* The comma (,) : This operator specifies a list of values
* The dash (-) : This operator specifies a range of values
* The separator (/) : This operator specifies a step value

For example, if we want `client/downstream.py` to be executed every 2 hours, we should enter:

    0 */2 * * * /path/to/command/client/downstream.py
    
For more details about cron, please click [here](http://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/).

## RESTful API Specification
### Get index

1. Request

        GET /

2. Parameters

    None

3. JSON Result

        {'message': 'Please refer to our api'}
    
4. Curl Example

        curl -X GET http://localhost:5000/


### Ping the server
A simple ping request to let you know things are working.

1. Request

        GET /ping

2. Parameters

    None

3. JSON Result

        {"message": "PONG"}

4. Curl Example

        curl -X GET http://localhost:5000/ping

### Getting your ip address
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

### Get silos list
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


### Get silo
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

### Update  silo
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


### Delete silo
To delete a silo by silo id.

1. Request

        DELETE /silos/silo_id

2. Parameters

        silo_id

3. JSON Result

    None

4. Curl Example

        curl -X DELETE http://localhost:5000/silos/silo1