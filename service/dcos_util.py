"""
Utility functions for DCOS.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-04-02
@status: init
"""

import os
import logging
import json
import uuid
import requests

FOB_PORT = 9999
FOB_PREFIX = "fob-aviary/"
FUN_DIR = "funcache/"

def service_loc(marathon_api):
    """
    Retrieves the IP:PORT of the fob service.
    """
    op_url = "".join([marathon_api, "/v2/apps/fob"])
    logging.debug("OPERATION: %s" %(op_url))
    res = requests.request('GET', op_url)
    logging.debug("RESPONSE:\n%s" %(res.json()))
    fob_host = res.json()["app"]["tasks"][0]["host"]
    fob_port = res.json()["app"]["tasks"][0]["ports"][0]
    return "".join(["http://", fob_host, ":", str(fob_port)])

def register_fun(marathon_api, template_filename, code_snippet):
    """
    Registers a function by launching a container using the Marathon API.
    All functions live in a group specified by `FOB_PREFIX`.
    Since the service is stateless, Marathon is leveraged to keep the state around.
    """
    op_url = "".join([marathon_api, "/v2/apps"])
    logging.debug("OPERATION: %s" %(op_url))
    
    # rather than a name, each function gets a unique ID assgined by which
    # it is known system-wide. the actual code of the function (aka as the code snippet) 
    # is also available via this unique ID:
    fun_id = str(uuid.uuid4())
    logging.debug("Generating function %s" %(fun_id))
    
    # make sure the code snippet is stored in the local
    # filesystem so that the driver later on can download it:
    if not os.path.exists(FUN_DIR): 
        os.makedirs(FUN_DIR)
    code_snippet_filename = os.path.join(FUN_DIR, fun_id)
    with open(code_snippet_filename, "w") as code_snippet_file:
        code_snippet_file.write(code_snippet)
    logging.debug("Function %s is cached now" %(fun_id))

    # now let's fill in the provided template:
    with open(template_filename) as f:
        payload = json.load(f)
        payload["id"] = "".join([FOB_PREFIX, fun_id])
        
        # the following is language/driver specific:
        fob_service = service_loc(marathon_api)
        code_snippet_url = "".join([fob_service, "/api/cs/", fun_id])
        logging.debug("The function is available via %s" %(code_snippet_url))
        payload["cmd"] = "".join(["curl ", code_snippet_url, " > fobfun.py && python fob_driver.py"])
        
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
    fun_meta = {
        "host" : res.json()["app"]["tasks"][0]["host"],
        "port" : res.json()["app"]["tasks"][0]["ports"][0]
    }
    return (res, fun_meta)

def call_fun(marathon_api, fun_id, fun_param):
    """
    Calls a function using the Marathon API.
    """
    (res, fun_meta) = about_fun(marathon_api, fun_id)
    
    if fun_param:
        op_url = "".join(["http://", fun_meta["host"], ":", str(fun_meta["port"]), "?params=", fun_param])
    else:
        op_url = "".join(["http://", fun_meta["host"], ":", str(fun_meta["port"])])
    logging.debug("OPERATION: %s" %(op_url))
    res = requests.request('GET', op_url)
    logging.debug("RESPONSE:\n%s" %(res.json()))
    return res.json()["result"]

def get_fun_code(fun_id):
    """
    Retrieves the code of a function.
    """
    code_snippet_filename = os.path.join(FUN_DIR, fun_id)
    code_snippet = ""
    with open(code_snippet_filename) as f:
        code_snippet = f.read()
    return code_snippet

def list_fun(marathon_api):
    """
    Retrieves a list of all registered functions under the `FOB_PREFIX` using the Marathon API.
    """
    op_url = "".join([marathon_api, "/v2/groups/", FOB_PREFIX])
    logging.debug("OPERATION: %s" %(op_url))
    res = requests.request('GET', op_url)
    logging.debug("RESPONSE:\n%s" %(res.json()))
    fun_list = []
    if res.json()["apps"]:
        apps = res.json()["apps"]
        for app in apps:
            logging.debug("Registered function %s" %(app["id"]))
            fun_list.append(app["id"].split("/")[2])
    return fun_list
