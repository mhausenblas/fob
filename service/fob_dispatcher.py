#!/usr/bin/env python

"""
Flock of birds POC.

Usage (especially for testing):

    $ export MARATHON_API=http://localhost:8080
    $ python fob_dispatcher.py

If the env variable MARATHON_API is not set, the service assumes
it runs in a DCOS cluster and uses http://master.mesos/service/marathon
 

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2016-04-02
@status: init
"""

import logging
import os
import json
import tornado.ioloop
import tornado.web
import dcos_util

from tornado.escape import json_encode


DEBUG = True
FOB_PORT = 9999
PROD_MARATHON_API = "http://master.mesos/service/marathon"
MARATHON_API = ""

if DEBUG:
  FORMAT = "%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]"
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")
else:
  FORMAT = "%(asctime)-0s %(message)s"
  logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")

class StatsHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Provides an overview of the registered functions.
        """
        res = "fob up"
        self.set_header("Content-Type", "application/json")
        self.write({
                "status" : res
        })

class GenerateFunHandler(tornado.web.RequestHandler):
    def post(self):
        """
        Takes the POSTed code snippet and launches a container with it.
        """
        lang_arg = self.get_query_argument(name="lang", default="python", strip=True)
        code_snippet = self.request.body
        logging.info("Trying to launch code snippet, interpreting it as [%s]" %(lang_arg))
        logging.debug("\n%s" %(code_snippet))
        try:
            (res, fun_id) = dcos_util.register_fun(MARATHON_API, "templates/python_sandbox.json", code_snippet)
            self.set_header("Content-Type", "application/json")
            self.write({
                "id" : fun_id
            })
        except Exception as err:
            logging.debug("Something went wrong when launching the sandbox:\n%s" %(str(err)))
            self.set_status(404)

class MetaFunHandler(tornado.web.RequestHandler):
    def get(self, fun_id):
        """
        Provides information on a registered functions.
        """
        logging.info("Trying to look up function %s" %(fun_id))
        res = dcos_util.about_fun(MARATHON_API, fun_id)
        self.set_header("Content-Type", "application/json")
        self.write(res.json())

def _make_app():
    """
    Set up the API handler.
    """
    return tornado.web.Application([
        (r"/api/stats", StatsHandler),
        (r"/api/gen", GenerateFunHandler),
        (r"/api/meta/(.*)", MetaFunHandler)
    ])

if __name__ == "__main__":
    
    MARATHON_API = os.getenv('MARATHON_API', PROD_MARATHON_API)
    app = _make_app()
    app.listen(FOB_PORT)
    logging.info("FOB dispatcher ready ===")
    logging.info("Using Marathon API %s" %(MARATHON_API))
    logging.info("Listening on port %d" %(FOB_PORT))
    
    tornado.ioloop.IOLoop.current().start()