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

DEBUG = True
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
        Executes a Python code snippet
        """
        res = fobfun.callme()
        self.write({
            "result" : res
        })

if __name__ == "__main__":
    app = tornado.web.Application([(r"/", DriverHandler)])
    app.listen(FOB_DRIVER_PORT)
    tornado.ioloop.IOLoop.current().start()