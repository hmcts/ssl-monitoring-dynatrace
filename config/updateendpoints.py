#!/usr/bin/env python

import yaml
import requests
import json
from urllib import request as url_request


a_yaml_file = open("./nonprod/calculated-metrics-service/calculated-metrics-service-copy.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
#for token in parsed_yaml_file:
 #       print(token)

from typing import Iterable, Any, Tuple
def signal_last(it:Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var

def special_function(var):
   print("Special function var is:"+var)

def not_so_special_function(var):
   print("Not so Special function var is:"+var)




csm_metrickeys_domainin = ''
csm_metrickeys_domainout = ''
for doc in parsed_yaml_file["config"]:
       for k, v in doc.items():
         for mappings in parsed_yaml_file[k]:
            for x, y in mappings.items():
              if x=='metric_key':
                if 'ssldomainin' in y:
                 csm_metrickeys_domainin=csm_metrickeys_domainin+y+","
                else: 
                 csm_metrickeys_domainout=csm_metrickeys_domainout+y+","

print(csm_metrickeys_domainin)
print(csm_metrickeys_domainout)

filepath = './nonprod/sslchecker-endpoint/sslCheckerEndpointTemplate.json'
with open(filepath) as fh:
   mydata = fh.read()
   data_json = json.loads(mydata)
   for k,v in data_json["properties"].items():
        if k=='OutboundMetricNames':
           v+=csm_metrickeys_domainout
        if k=='InboundMetricNames':
           v+=csm_metrickeys_domainin
   print(data_json)
   response = requests.put('https://yrk32651.live.dynatrace.com/api/config/v1/plugins/custom.remote.python.sslCheck/endpoints/6691303106622817277',
      data=mydata,                         
      headers={'content-type':'application/json','Authorization': 'Api-Token I1RtfySETHGKBGasu0Q-e'},
      params={'file': filepath},
      allow_redirects=True
    )
   print(response)
