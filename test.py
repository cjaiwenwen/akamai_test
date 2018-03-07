import requests
from urlparse import urljoin
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
from http_calls import EdgeGridHttpCaller
debug = True
verbose = False

section_name = "default"

config = EdgeGridConfig({"verbose":False},section_name)
baseurl = '%s://%s/' % ('https', config.host)

s = requests.Session()

s.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

httpCaller = EdgeGridHttpCaller(s, debug, verbose, baseurl)

#result = httpCaller.getResult('/diagnostic-tools/v2/ghost-locations/available')
#result = s.get(urljoin(baseurl, '/diagnostic-tools/v1/locations'))

result = s.get(urljoin(baseurl, '/diagnostic-tools/v1/locations'))

print result.status_code

location =  result.json()['locations'][0]['id']

dig_parameters = { "hostName":"junchen.sandbox.akamaideveloper.com"}

dig_result = httpCaller.getResult("/diagnostic-tools/v2/ghost-locations/%s/dig-info" % location,dig_parameters)

# Display the results from dig
print (dig_result['digInfo'])

cloudlet_result = httpCaller.getResult("/cloudlets/api/v2/cloudlet-info")

print cloudlet_result.json()
