#!/usr/bin/env python

import yaml
import requests
import json
import os
from urllib import request as url_request

dynatrace_plugin="custom.remote.python.sslCheck"
endpointname= "fees & pay"
base_url="https://yrk32651.live.dynatrace.com"
plugin_module_id="4579337562609868372"
activegate_instance_name="activegate-nonprod-vmss000003"

a_yaml_file = open("../nonprod/calculated-metrics-service/calculated-metrics-service.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
#for token in parsed_yaml_file:
 #       print(token)

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

dynatrace_api_key = os.environ["api_key"]
dynatrace_registration_method = "PUT"
dynatrace_req_headers = {"Authorization": "Api-token {}".format(dynatrace_api_key)}
dynatrace_req_headers["Content-Type"] = "application/json"
dynatrace_registration_req_data = {"pluginId": dynatrace_plugin, "name": endpointname, "enabled": True,
                                    "properties": {"ClusterAddress": base_url,
                                                  "ExpirationDelta": "10", "DomainsToIgnore": "",
                                                  "ApiToken": "{}".format(dynatrace_api_key),"OutboundMetricNames":csm_metrickeys_domainout,"InboundMetricNames":csm_metrickeys_domainout},
                                    "activeGatePluginModule": {"id": plugin_module_id, "name": activegate_instance_name}}
dynatrace_registration_data = json.dumps(dynatrace_registration_req_data).encode("utf-8")
dynatrace_registration_url = 'https://yrk32651.live.dynatrace.com/api/config/v1/plugins/custom.remote.python.sslCheck/endpoints/6691303106622817277'
dynatrace_registration_req = url_request.Request(url=dynatrace_registration_url,
                                                  data=dynatrace_registration_data,
                                                  headers=dynatrace_req_headers, method=dynatrace_registration_method)
                                                  
with url_request.urlopen(dynatrace_registration_req, timeout=120) as response:
    print("Plugin endpoint {} complete: status={}, reason={}".format(dynatrace_registration_method, response.status, response.reason))
