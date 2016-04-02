"""
Utility functions for DCOS.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-04-02
@status: init
"""

import json 
import requests

def launch_app(marathon_api, template_filename):
    """
    Launches a DCOS app using the Marathon API.
    """
    op_url = "".join([marathon_api, "/v2/apps"])
    with open(template_filename) as f:
        payload = f.read()
        res = requests.request('POST', op_url, data=payload)
        logging.debug("RESPONSE:\n%s" %(res.json()))
    return res
