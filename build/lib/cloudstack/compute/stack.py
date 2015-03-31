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
import hashlib

class Stack(object):
    def __init__(self, http, host, api_key, secret_key):
        self.http = http
        self.host = host
        self.api_key = api_key
        self.secret_key = secret_key

    def signature(self, command, query):
        query['command'] = command
        query['apikey'] = self.api_key
 
        if not query or not query.has_key('response'):
            query['response'] = 'json'

        query_str = '&'.join(['='.join(
                    [k,urllib.quote_plus(query[k]).replace('+', '%20')]
                    ) for k in query.keys()])
        signature_str = '&'.join(['='.join(
                    [k.lower(),
                    urllib.quote_plus(query[k]).replace('+','%20').lower()
                    ]
                    )for k in sorted(query.iterkeys())])
        signature = urllib.quote_plus(
                      base64.encodestring(hmac.new(self.secret_key,signature_str,hashlib.sha1).digest()).strip()
                    )
        return (query_str, signature)

    def url(self, command, query):
        quoted_query, signature = self.signature(command,query)
        return "%s?%s&signature=%s" % (self.host,
                                       quoted_query,
                                       signature)

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
