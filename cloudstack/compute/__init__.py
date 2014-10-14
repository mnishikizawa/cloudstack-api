from cloudstack.compute.shell import API_REFS
from cloudstack.utils import res, dict2obj
import client
import urllib
import sys

def valid_methods():
    return [r['name'] for r in API_REFS]

class Method(object):
    def __init__(self, command, method_name):
        self.command = command
        self.method_name = method_name

    def __call__(self, **kwargs):
        api = [f for f in API_REFS if f['name'] == self.method_name]
        if not api:
            print '[%s] method is not suuported.' % self.method_name
            return
        options = api[0]['options']
        required_opt = [opt['option'][2:] for opt in options
                        if opt['required'] == 'true']
        missing = set(required_opt) - set(kwargs.keys())
        if missing:
            print '[%s] option is required.' % ', '.join(list(missing))
            return

        params = dict([(k,v) for (k,v) in kwargs.items()
                     for opt in options
                     if opt['option'][2:] == k])

        json = client.connect(host=self.command.host,api_key=self.command.api_key,
                              secret_key=self.command.secret_key,debug=self.command.debug
                              ).get(self.method_name,params)
        if json:
            retval = dict2obj(json[json.keys()[0]])
            if retval and  hasattr(retval,'list'):
                return retval.list
            else:
                return retval

class Compute(object):
    def __init__(self,host=None,api_key=None,secret_key=None,api_refs_json=None,debug=False):
        self.host = host
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_refs_json = api_refs_json
        self.debug = debug

    def __getattr__(self,method_name):
        return Method(self,method_name)

    def methods(self):
        return valid_methods()
