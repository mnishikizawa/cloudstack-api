#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson

str =  sys.stdin.readline().strip()
json = simplejson.loads(str)
print simplejson.dumps(json,sort_keys=True, indent=2)
