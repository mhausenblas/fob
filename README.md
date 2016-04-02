# Flock of Birds (fob)

Flock of Birds is a proof-of-concept for a serverless offering based on [DCOS](https://docs.mesosphere.com/).
It is not meant to be used in production. Its purpose is to illustrate and study the properties of
[serverless compute architectures](http://flock-of-birds.info/).


## Prerequisites 

For the following to work, I'm assuming you've got a DCOS cluster provisioned and the [DCOS CLI](https://docs.mesosphere.com/administration/cli/) installed. Note: you want to have [jq](https://stedolan.github.io/jq/) installed, otherwise you'd need to use `grep` for certain CLI interactions.
Also, I'm using [http](http://httpie.org) for HTTP API interactions, if you don't have this or want it, you can use the respective `curl` commands instead.

## Installation

In order to use the Flock of Birds service, you need to clone this repo locally (especially if you want to do experiments around it):

    $ git clone https://github.com/mhausenblas/fob.git && cd fob/

To launch the Flock of Birds service, do the following:

    $ dcos marathon app add fob-service.json

To access the Flock of Birds service, you first have to figure out where it runs. It is configured to run on the public agent, and you'll need to look up its IP (this is dependent on your provider, such as Azure, AWS or a private cloud IaaS offering). I've looked up the public agent IP manually in the administration UI and captured its value in the environment variable `$DCOS_PUBLIC_AGENT`:

    $ echo $DCOS_PUBLIC_AGENT
    52.33.144.9

Next, you need to find out on which port the Flock of Birds service is running. This can be achieved using the following (requires `jq` command installed):

    $ FOB_SERVICE_PORT="$(dcos marathon app show fob | jq .tasks[0].ports[0])"
    $ echo $FOB_SERVICE_PORT
    7937

Now we have the address of the Flock of Birds service and can use it (using `http` command):

    $ http POST $DCOS_PUBLIC_AGENT:$FOB_SERVICE_PORT/api/gen < py_example.py

## Usage


## Testing

For local testing and development you first need to install dependencies (assuming you've got `pip` and `virtualenv` installed):

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
    Content-Length: 20
    Content-Type: application/json; charset=UTF-8
    Date: Sat, 02 Apr 2016 23:10:41 GMT
    Etag: "8af23ae30ba92d44d1a5335a5fc59f73e28588cc"
    Server: TornadoServer/4.3

    {
        "status": "fob up"
    }

You can register a code snippet (function) like so:

    $ http POST http://localhost:9999/api/gen < ../py_example.py
    HTTP/1.1 200 OK
    Content-Length: 46
    Content-Type: application/json; charset=UTF-8
    Date: Sat, 02 Apr 2016 23:09:47 GMT
    Server: TornadoServer/4.3

    {
        "id": "0e38b688-86e3-4966-9060-cf01eef59426"
    }

Then, you can query its status like so:

    $ http http://localhost:9999/api/meta/0e38b688-86e3-4966-9060-cf01eef59426
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
