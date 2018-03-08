#!/usr/bin/env python

import requests
from urlparse import urljoin
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from config import EdgeGridConfig
from http_calls import EdgeGridHttpCaller
import random

debug = False
verbose = False

edgerc = EdgeRc("$WORKSPACE/.edgerc")

section_name = "default"

config = EdgeGridConfig({"verbose":False},section_name)
baseurl = '%s://%s/' % ('https', config.host)

s = requests.Session()

s.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

httpCaller = EdgeGridHttpCaller(s,debug,verbose,baseurl)

result = httpCaller.getResult(urljoin(baseurl, '/diagnostic-tools/v2/ghost-locations/available'))

location_list = []
for item in result['locations']:
    location_list.append(item['id'])

print location_list

print "[*] There are %s places that we could resolve from"%(len(location_list))

location = random.choice(location_list)

print "[*] process to resolve %s from country %s"%("junchen.sandbox",location)

dig_parameters = { "hostName":"junchen.sandbox.akamaideveloper.com"}


dig_result = httpCaller.getResult("/diagnostic-tools/v2/ghost-locations/%s/dig-info" % location,dig_parameters)

# Display the results from dig
print (dig_result['digInfo']['result'])
