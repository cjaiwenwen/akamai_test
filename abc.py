#!/usr/bin/env python

import requests
from urlparse import urljoin
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from config import EdgeGridConfig
from http_calls import EdgeGridHttpCaller
import random
import json

debug = False
verbose = False

section_name = "default"
section_ccu = "ccu"

edgerc = EdgeRc("/var/jenkins_home/workspace/akamai_test/.edgerc")

#config = EdgeGridConfig({"verbose":False},section_name)
#baseurl = '%s://%s/' % ('https', config.host)
baseurl = 'https://%s'%edgerc.get(section_name, 'host')

s = requests.Session()
t = requests.Session()
#s.auth = EdgeGridAuth(
#            client_token=config.client_token,
#            client_secret=config.client_secret,
#            access_token=config.access_token
#)

s.auth = EdgeGridAuth.from_edgerc(edgerc, section_name)

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

#config_t = EdgeGridConfig({"verbose":False},section_ccu)
#baseurl = '%s://%s/' % ('https', config.host)
baseurl_t = 'https://%s'%edgerc.get(section_ccu, 'host')

t.auth = EdgeGridAuth.from_edgerc(edgerc, section_ccu)

httpCaller_t = EdgeGridHttpCaller(t,debug,verbose,baseurl_t)

purge_obj = {
	"objects" : [
		"https://khunter.sandbox.akamaideveloper.com/index.html"
	]
}

print ("Adding invalidate request to queue - %s" % (json.dumps(purge_obj)));

purge_post_result = httpCaller_t.postResult('/ccu/v3/invalidate/url', json.dumps(purge_obj))

print purge_post_result
