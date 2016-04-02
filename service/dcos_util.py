"""
Utility functions for DCOS.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-04-02
@status: init
"""

import logging
import json
import uuid
import requests

FOB_PREFIX = "fob-aviary/"

def register_fun(marathon_api, template_filename, code_snippet):
    """
    Registers a function by launching a container using the Marathon API.
    """
    op_url = "".join([marathon_api, "/v2/apps"])
    logging.debug("OPERATION: %s" %(op_url))

    with open(template_filename) as f:
        payload = json.load(f)
        fun_id = str(uuid.uuid4())
        payload["id"] = "".join([FOB_PREFIX, fun_id])
        logging.debug("INSTANCE:\n%s" %(payload))
        res = requests.request('POST', op_url, data=json.dumps(payload))
        logging.debug("RESPONSE:\n%s" %(res.json()))
    return (res, fun_id)

def about_fun(marathon_api, fun_id):
    """
    Provides info about a function using the Marathon API.
    """
    op_url = "".join([marathon_api, "/v2/apps/", FOB_PREFIX, fun_id])
    logging.debug("OPERATION: %s" %(op_url))
    res = requests.request('GET', op_url)
    logging.debug("RESPONSE:\n%s" %(res.json()))
    return res
