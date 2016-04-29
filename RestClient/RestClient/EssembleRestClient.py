import sys
import ssl
import urllib
import urllib2
import json
import time

from unidecode import unidecode 
from pprint import pprint

class EssembleRestClient(ob ject):
    def __init__(self, server='https://localhost:6443/arcgis/rest/services', reqs_per_sec=15):
        self.server = server
        self.reqs_per_sec = reqs_per_sec
        self.req_count = 0
        self.last_req = 0

    def perform_rest_action(self, endpoint, params=None, hdrs=None):
        if hdrs is None:
            hdrs = {}

        if 'Content-Type' not in hdrs:
            hdrs['Content-Type'] = 'application/json'

        if params:
            endpoint += '?' + urllib.urlencode(params)

        data = None

        # check if we need to rate limit ourselves
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                time.sleep(1 - delta)
            self.last_req = time.time()
            self.req_count = 0

        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            full_url = self.server + endpoint
            request = urllib2.Request(full_url, headers=hdrs)
            response = urllib2.urlopen(request)
            content = response.read()
            if content:
                data = json.loads(content)
            self.req_count += 1

        except urllib2.HTTPError as e:
            # check if we are being rate limited by the server
            if e.code == 429:
                if 'Retry-After' in e.headers:
                    retry = e.headers['Retry-After']
                    time.sleep(float(retry))
                    self.perform_rest_action(endpoint, hdrs, params)
            else:
                sys.stderr.write('Request failed for {0}: Status code: {1.code} Reason: {1.reason}\n'.format(endpoint, e))

        return data

    def hit_server(self, serviceName, bFeatureService, operation, params):
        featureService = "FeatureServer"
        if not bFeatureService:
            featureService = "AQS"
        endpoint = '/{0}/{1}/0/{2}'.format( serviceName, featureService, operation)
        response = self.perform_rest_action( endpoint, params )
        if response:
            #str = json.dumps(response).replace("u\"","\"").replace("u\'","\'")            
            str = unidecode(json.dumps(response).decode('utf8'))
            
            nice = json.loads(str)
            #str = response.replace("u\"","\"").replace("u\'","\'")
            pprint(nice)


