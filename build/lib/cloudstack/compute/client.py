#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import optparse
import httplib2
import time
import os
import sys
import ConfigParser
from cloudstack.utils import safe_option
from stack import Stack

API_CONF_PATH = os.path.join(os.path.expanduser("~"),".idcfrc")
logging.basicConfig(format="%(asctime)s %(module)s[%(lineno)d] [%(levelname)s]: %(message)s",
                    #filename = "log.txt",
                    level=logging.INFO)

def connect(host=None,api_key=None,secret_key=None,debug=False):
    if debug:
        httplib2.debuglevel = 1
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        httplib2.debuglevel = 0
        logging.getLogger().setLevel(logging.INFO)

    http = httplib2.Http(disable_ssl_certificate_validation=True)
    config = ConfigParser.SafeConfigParser()
    config.read(API_CONF_PATH)

    try:
        if not host:
            host = os.environ.get('IDCF_COMPUTE_HOST')
            if not host:
                host = safe_option(config,"account", "host")
        if not api_key:
            api_key = os.environ.get('IDCF_COMPUTE_API_KEY')
            if not api_key:
                api_key = safe_option(config,"account", "api_key")
        if not secret_key:
            secret_key = os.environ.get('IDCF_COMPUTE_SECRET_KEY')
            if not secret_key:
                secret_key = safe_option(config,"account","secret_key")

    except ConfigParser.NoSectionError, e:
        print >> sys.stderr, e.message
        #f = open(API_CONF_PATH,"w")
        #config.add_section("account")
        #config.set("account", "host","http://xxx")
        #config.set("account", "api_key","xxx")
        #config.set("account","secret_key","xxx")
        #config.write(f)
        sys.exit(1)

    except Exception, e:
        print >> sys.stderr, e
        sys.exit(1)
    return Stack(http,host,api_key,secret_key)
