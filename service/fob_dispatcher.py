#!/usr/bin/env python

"""
Flock of birds POC

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


DEBUG = False
FOB_PORT = 9999
MARATHON_API = "http://master.mesos/service/marathon"

if DEBUG:
  FORMAT = "%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]"
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")
else:
  FORMAT = "%(asctime)-0s %(message)s"
  logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%dT%I:%M:%S")


class GenerateFunHandler(tornado.web.RequestHandler):
    def post(self):
        """
        Takes the POSTed code snippet and launches a container with it.
        """
        lang_arg = self.get_query_argument(name="lang", default="python", strip=True)
        code_snippet = self.request.body
        logging.info("Trying to launch code snippet, interpreting it as [%s]" %(lang_arg))
        logging.debug("%s" %(code_snippet))
        try:
            res = dcos_util.launch_app(MARATHON_API, "templates/python_sandbox.json")
            self.set_header("Content-Type", "application/json")
            self.write(json_encode(res))
        except:
            logging.debug("Can't reach DCOS cluster")
            self.set_status(404)

def _make_app():
    """
    Set up the API handler.
    """
    return tornado.web.Application([
        (r"/api/gen", GenerateFunHandler)
    ])

if __name__ == "__main__":
    app = _make_app()
    app.listen(FOB_PORT)
    logging.info("FOB dispatcher ready. Listening on port %d" %(FOB_PORT))
    tornado.ioloop.IOLoop.current().start()