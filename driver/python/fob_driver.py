#!/usr/bin/env python

"""
Flock of birds Python driver.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-04-02
@status: init
"""

import logging
import os
import json
import tornado.ioloop
import tornado.web
import fobfun

from tornado.escape import json_encode

DEBUG = False
FOB_DRIVER_PORT = 8080

if DEBUG:
  FORMAT = "%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]"
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")
else:
  FORMAT = "%(asctime)-0s %(message)s"
  logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")

class DriverHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Executes a Python code snippet. The function that is called must be in module `fobfun`
        and it must be called `callme`. Any parameters that are present in the request URL
        will be passed onto the `callme` function. Format is `params=param1:val1,param2:val2,...`.
        For example, if the request URL is:
        
            http://localhost:8080?params=param1:42,param2:this%20is
        
        then the the following is executed: fobfun.callme(param1=42, param2='this is').
        As usual, the parameter values need to be encoded as per RFC3986 https://tools.ietf.org/html/rfc3986
        """
        try:
            params = self.get_query_argument(name="params", default="", strip=True)
            logging.debug("Raw query parameters %s" %(params))
            params = params.split(",")
            params = {k:v for k,v in (p.split(':') for p in params) }
            logging.info("Got parameters %s" %(params))
            res = fobfun.callme(**params)
            self.write({
                "result" : res
            })
        except Exception as err:
            logging.debug("Something went wrong executing the code snippet:\n%s" %(str(err)))
            self.write({
                "result" : "No or wrong parameters supplied, can not execute the code snippet."
            })
            self.set_status(404)
        

if __name__ == "__main__":
    app = tornado.web.Application([(r"/", DriverHandler)])
    app.listen(FOB_DRIVER_PORT)
    tornado.ioloop.IOLoop.current().start()