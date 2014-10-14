# -*- coding: utf-8 -*-
import logging

import urllib
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, message=r'the sha module')
import sha
import hmac
import base64
import os
import simplejson
from lxml import etree
import httplib2

class Stack(object):
    def __init__(self, http, host, api_key, secret_key):
        self.http = http
        self.host = host
        self.api_key = api_key
        self.secret_key = secret_key

    def signature(self, command, query):
        query_params = dict(command=command)

        if not query or not query.has_key('response'):
            query['response'] = 'json'

        query_params.update([q.replace('+','%20').split("=") for q in
                             urllib.urlencode(query).split("&")])
        quoted_query = "&".join(["%s=%s" % (k,v) for (k,v) in query_params.items()])

        params = dict([(k,v.lower()) for (k,v) in query_params.items()])
        params["apiKey".lower()] = self.api_key.lower()
        msg = "&".join(["%s=%s" % (k,v) for (k,v) in sorted(params.items())])
        hashed = hmac.new(self.secret_key, msg, sha)
        return (quoted_query, urllib.quote(base64.b64encode(hashed.digest())))

    def url(self, command, query):
        quoted_query, signature = self.signature(command,query)
        return "%s?%s&apiKey=%s&signature=%s" % (self.host,
                                                 quoted_query,
                                                 self.api_key, signature)

    def connect(self, method, command, query):
        try:
            url = self.url(command,query)
            response, content = self.http.request(url, method=method)
            logging.debug("status  : %d"% response.status)
            if query['response'] == 'json':
                return simplejson.loads(content)
            else:
	        parser = etree.XMLParser()
                tree = etree.XML(content, parser)
                return content
        except httplib2.ServerNotFoundError,e:
            print e
        except etree.XMLSyntaxError:
            print content
        except ValueError:
            print content

    def get(self, command, query=None):
        return self.connect('GET',command,query)
