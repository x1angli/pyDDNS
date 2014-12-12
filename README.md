DDNS-chiasma
============

A Dynamic DNS system used to update DNS records.

# Introduction
This python project Contains the following three modules:

1. Upstream

    The upstream machine normally has an ever-changing IP. To dynamically tracking the upstream machine's IP, we need to execute the upstream Python module intermittently. At such times, the `client/upstream` module is used on the upstream machine.

    Once the `client/upstream` module is executed, it sends a `Get /silos/silo_id` request to retrieve the IP of itself. If the IP address has changed, it will continue to send a `PUT /silos/silo_id` request to update DNS records of silos specified in `client/config.yml`.

    `Silo` is used to record the DNS information. Each silo has a unique ID, and each ID corresponds to a sever. The silo may contiains more than one DNS record, and each DNS record contains hostname and IP address. You can get different silo information by different RESTful API on the server.

    `Client/config.yml` is a YAML file to store the server and DNS details. Besides, it also provides an entry named `getIpFrom`. If the upstream machine has an independent public IP, `getIpFrom` should be set to `Socket`, otherwise, it should be set to `ServerApi`.

    So finally, we can get a latest `client/config.yml` file on the upstream machine.

2. Downstream

    On the upstream machine, we just get a latest YAML file but not the local host file which stores DNS rules, so we must execute `client/downstream` module on the downstream machine.

    `Client/downstream` module can get DNS records of silos specified in `client/config.yml` by sending `Get /silos/silo_id` request. And then, it will modify the DNS rules in the local host file to the latest version without any manual modification.

3. Server

    As a sever, it should have a static IP. What's more, it is necessary for the server to install a database like SQLite or MySQL.

    `Server` module is used on the sever. It uses web framework 'Flask' to build RESTful APIs, so that we can get client IP, get silos list or maintain each silo by these APIs.

    Besides, there is also a YAML file named `client/config.yml` to store DB settings like `username` and `password`. You can modify these settings for your actual situation.

    For more details about RESTful APIs in `server`, please read the "RESTful API Specification" section.

## Installation
1. Make sure Python is properly installed on all your platforms (i.e. Server, Upstream, Downstream)
2. Modify the `/server/config.yml` file to change DB setting, and `/client/config.yml` file to specify Server and DNS details
3. Execute following commands to install requirement environments and initialize your own database on server side:

        pip install -r requirements.txt
        flask --app=server.app initdb

## Start using the server
1. Execute following commands:

        cd DDNS-chiasma
        set PYTHONPATH=%PYTHONPATH%;.
        python server/app.py

2. Open your browser, visit `http://localhost:81/ping`, and you would get the ping-pong JSON.That means your server successfully started up
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
The set command above is executed in Windows environment. But in Linux environment, the command, reference and separator for environment variable to set PYTHONPATH are different.

1. Windows
    * use `set` command
    * use `% %` to reference the environment variable
    * use `;` as the separator

            set PYTHONPATH=%PYTHONPATH%;.

2. Linux
    * use `export` command
    * use `$` to reference the environment variable
    * use `:` as the separator

            export PYTHONPATH=$PYTHONPATH:.

Please use the correct command to set PYTHONPATH according to your system environment.

## How to run it automatically
If you want to run the system automatically, please read this section and follow the instructions to set your computer settings.

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

The operations above are performed in Windows 7 environment. There may be a little different in other Windows environments, please operate in the light of actual conditions. For more details about Task Scheduler, please click [here][scheduler].

### Cron job in Linux
Cron job are used to schedule commands to be executed periodically. You can setup commands or scripts, which will repeatedly run at a set time. Cron is one of the most useful tool in Linux.

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

operator allows you to specifying multiple values in a field. There are three operators:
* The asterisk (*) : This operator specifies all possible values for a field
* The comma (,) : This operator specifies a list of values
* The dash (-) : This operator specifies a range of values
* The separator (/) : This operator specifies a step value

For example, if we want `client/downstream.py` to be executed every 2 hours, we should enter:

    0 */2 * * * /path/to/command/client/downstream.py

For more details about cron, please click [here][cron].

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
This RESTful API allows you to know things are working.

1. Request

        GET /ping

2. Parameters

    None

3. JSON Result

        {"message": "PONG"}

4. Curl Example

        curl -X GET http://localhost:5000/ping

### Getting your IP address
This RESTful API allows you to get your current public IP address.
Plese note that this API may not work correctly if you are behind a proxy.

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
