# Development

In order to do local testing, development and experiment with the Flock of Birds service, you need to clone this repo locally:

    $ git clone https://github.com/mhausenblas/fob.git && cd fob/

I will assume you've got `pip` and `virtualenv` installed as well.

## Service

First you need to install dependencies :

    $ cd service
    $ virtualenv env
    $ . env/bin/activate
    $ pip install -r requirements.txt

Once the environment is set up, you can launch the Flock of Birds service as shown in the following (using your local Marathon API or replace `MARATHON_API` with the cluster URL you're using):

    $ export MARATHON_API=http://pool-7830-elasticl-cv29rf2oafkv-1899442518.us-west-2.elb.amazonaws.com/service/marathon
    $ python fob_dispatcher.py
    2016-04-02T02:41:44 INFO FOB dispatcher ready === [at line 82]
    2016-04-02T02:41:44 INFO Using Marathon API http://pool-7830-elasticl-cv29rf2oafkv-1899442518.us-west-2.elb.amazonaws.com/service/marathon [at line 83]
    2016-04-02T02:41:44 INFO Listening on port 9999 [at line 84]

Now open up another terminal where you interact with the Flock of Birds service:

    $ http http://localhost:9999/api/stats
    HTTP/1.1 200 OK
    Content-Length: 95
    Content-Type: application/json; charset=UTF-8
    Date: Sun, 03 Apr 2016 18:20:36 GMT
    Etag: "6d8cffc288d757a408aa7874dbfde0a6c62f3542"
    Server: TornadoServer/4.3

    {
        "functions": [
            "2f0f7017-91eb-45a5-a07d-79c0b7c8a143",
            "4d2696d1-7cdc-4138-89e7-613ac5e9cbd4"
        ]
    }

You can register a code snippet (function) like so:

    $ http POST http://localhost:9999/api/gen < ../examples/python/example.py
    HTTP/1.1 200 OK
    Content-Length: 46
    Content-Type: application/json; charset=UTF-8
    Date: Sat, 02 Apr 2016 23:09:47 GMT
    Server: TornadoServer/4.3
    
    {
        "id": "2f0f7017-91eb-45a5-a07d-79c0b7c8a143"
    }

Then, you can query the function status like so:

    $ http http://localhost:9999/api/meta/2f0f7017-91eb-45a5-a07d-79c0b7c8a143
    HTTP/1.1 200 OK
    Content-Length: 37
    Content-Type: application/json; charset=UTF-8
    Date: Sat, 02 Apr 2016 23:35:03 GMT
    Etag: "b69f36130995a150445c04026c126e8cf9d069c7"
    Server: TornadoServer/4.3
    
    {
        "host": "10.0.6.172",
        "port": 25974
    }


## Driver

To execute a code snippet, the Flock of Birds service uses drivers. These are programming language-dependent sandboxes and are located in [driver/](driver/). Currently the following drivers are available:

- [Python driver](driver/python/), allowing to execute 2.7 code
- TBD: Node.js
