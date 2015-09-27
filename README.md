pyDDNS
============

A Dynamic DNS system used to update DNS records based on Python.

# Introduction
This Python project contains the following three modules:

1. Upstream

    The upstream unit has an ever-changing IP. To dynamically tracking the upstream machine's IP, we need to execute the `client/upstream` Python module on the upstream unit. Once the `client/upstream` module is executed, it either sends a `Get /silos/silo_id` request to retrieve the IP of itself, or attempts to get an IP address from one of the network adaptors. If the IP address has changed, it will go ahead sending a `PUT /silos/silo_id` request to update DNS records under the silo specified in `client/config.yml`.(Here, a `Silo` means a group of DNS records. Each silo has a unique ID and one or more DNS record entry, and each DNS record entry contains a hostname and an IP address.)

2. Downstream

    The downstream unit usually needs to communiate with the upstream unit, so it needs to know the current IP address of the upstream unit. To achieve this, we need to executed the `client/downstream` module on the downstream unit. Once it is executed, it can get all DNS records of a silo. And then, it will modify the hosts file to update relevant DNS records on the downstream unit. 

3. Server

    The server is the "central hub" where all DNS records are stored, updated, and communicated. Thus, it should have a static IP. Once the `server` module is executed on the server, it essentially starts a Web Service provider that constantly communiates with the upstream and downstream units.

    In parcicular, a YAML file named `client/config.yml` are located in the server module to store DB connection info. The server module uses web framework 'Flask' to build RESTful APIs, so that we can get client IP, get silos list or maintain each silo by these APIs. For more details about RESTful APIs in `server`, please read the "RESTful API Specification" section.

## Installation
1. Make sure Python 3.x runtime is properly installed on all the paticipating units (i.e. the server, the upstream, and the downstream unit). Plus, a relational database should installed on the server unit.
2. Modify the `/server/config.yml` file to change DB setting, and `/client/config.yml` file to specify Server and DNS details
3. Execute following commands to install required Python packages and initialize your own database on server side:

        pip install -r requirements.txt
        flask --app=server.app initdb

## Start using the server
1. Execute following commands:

        cd pyDDNS
        set PYTHONPATH=%PYTHONPATH%;.
        python server/app.py

2. Open your browser, visit `http://localhost:81/ping`, and you would get the ping-pong JSON.That means your server successfully started up
3. Alternatively, use `curl` to get it:

        curl -X GET http://localhost:81/ping

## Start using the client
### Downstream (The end user)
On the downstream machine, execute following commands

        cd pyDDNS
        set PYTHONPATH=%PYTHONPATH%;.
        python client/downstream.py

### Upstream (The unit with dynamic IP)
On the upstream machine, execute following commands:

        cd pyDDNS
        set PYTHONPATH=%PYTHONPATH%;.
        python client/upstream.py

#### Note
The `set` command above is for Windows only. But under Linux, the command, reference, and separator for the `PYTHONPATH` environment are different.

1. Windows
    * Use the `set` command;
    * Use `%` to refer the environment variable;
    * Use `;` as the separator;
    * Example: 

            set PYTHONPATH=%PYTHONPATH%;.

2. Linux
    * Use the `export` command; 
    * Use `$` to refer the environment variable;
    * Use `:` as the separator;
    * Example:

            export PYTHONPATH=$PYTHONPATH:.

Please use the correct command to set PYTHONPATH according to your system environment.

## How to run it automatically
If you want to run the system automatically, please read this section and follow the instructions to set your computer settings.

### Task Scheduler in Windows
Task Scheduler enables you to automatically perform routine tasks on a chosen computer. Task Scheduler does this by monitoring whatever criteria you choose to initiate the tasks and then executing the tasks when the criteria is met.

1. Open Task Scheduler by clicking the **Start** button, then click following items: **Control Panel**,  **System and Security**,  **Administrative Tools**, and finally **Task Scheduler**.
2. Click the **Action** menu, and then click **Create Basic Task**.
3. Type a name for the task and an optional description, and then click **Next**.
4. Do one of the following:
    * To select a schedule based on the calendar, click **Daily**, **Weekly**, **Monthly**, or **One time**, click **Next**; specify the schedule you want to use, and then click **Next**.
    * To select a schedule based on common recurring events, click **When the computer starts** or **When I log on**, and then click **Next**.
    * To select a schedule based on specific events, click **When a specific event is logged**, click **Next**; specify the event log and other information using the drop-down lists, and then click **Next**.
5. To schedule a program to start automatically, click **Start a program**, and then click **Next**.
6. Click **Browse** to find the program you want to start, and then click **Next**.
7. Click **Finish**.

The operations above are performed in Windows 7 environment. The procedure for other versions of Windows may be differnt. For further details on Task Scheduler, please click [here][scheduler].

### Cron job in Linux
Cron job is used to schedule commands to be executed periodically. You can setup commands or scripts, which will repeatedly run at a scheduled time. Cron is one of the most useful tool in Linux.

To edit your crontab file, type the following command at the Linux shell prompt:

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

Operators allow you to specifying multiple values in a field. There are three types operators:
* The asterisk (*) : indicates all possible values for a field
* The comma (,) : usually used between a list of values
* The dash (-) : specifies a range of values
* The separator (/) : specifies a step value

For example, if we want `client/downstream.py` to be executed every 2 hours, we should enter:

    0 */2 * * * /path/to/command/client/downstream.py

For more details about cron, please click [here][cron].

## RESTful API Specification
### Ping
This API does not provide any meaningful result, but the system administrator or end users can use it to see if the server is working.

1. Request

        GET /ping

2. Parameters

    None

3. JSON Result

        {"message": "PONG"}

4. Curl Example

        curl -X GET http://localhost:5000/ping

### Get your IP public address
This RESTful API allows you to get your current public IP address.
Plese note that this API may not return expected result when the API call are invoked through an HTTP proxy .

1. Request

        GET /ip

2. Parameters

    None

3. JSON Result

        {"ip": "127.0.0.1"}

4. Curl Example

        curl -X GET http://localhost:5000/ip

### Get silos list
This RESTful API allows you to get a complete silos list.

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
This RESTful API allows you to get a single silo by silo ID.

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

### Update silo
This RESTful API allows you to update a single silo by silo ID.

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
This RESTful API allows you to delete a single silo by silo ID.

1. Request

        DELETE /silos/silo_id

2. Parameters

        silo_id

3. JSON Result

    None

4. Curl Example

        curl -X DELETE http://localhost:5000/silos/silo1

[scheduler]: http://windows.microsoft.com/en-US/windows/schedule-task#1TC=windows-7 "Schedule a task"
[cron]: http://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/ "HowTo: Add Jobs To cron Under Linux or UNIX?"
