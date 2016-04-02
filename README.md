# Flock of Birds (fob)

Flock of Birds is a proof-of-concept for a serverless offering based on [DCOS](https://docs.mesosphere.com/).
It is not meant to be used in production. Its purpose is to illustrate and study the properties of
[serverless compute architectures](http://flock-of-birds.info/).


## Prerequisites 

For the following to work, I'm assuming you've got a DCOS cluster provisioned and the [DCOS CLI](https://docs.mesosphere.com/administration/cli/) installed. Note: you want to have [jq](https://stedolan.github.io/jq/) installed, otherwise you'd need to use `grep` for certain CLI interactions.
Also, I'm using [http](http://httpie.org) for HTTP API interactions, if you don't have this or want it, you can use the respective `curl` commands instead.

## Install

CLONE REPO https://github.com/mhausenblas/fob

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

## Example