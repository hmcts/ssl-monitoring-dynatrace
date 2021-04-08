#!/usr/bin/env python

import yaml
import requests
import json
import os
import sys
import getopt
from urllib import request as url_request

dynatrace_plugin="custom.remote.python.sslCheck"

def main(argv):
    """Script to update sslChecker plugin endpoint in Dynatrace for monitoring
    """

    usage = """update-sslchecker-plugin-endpoint.py -d <dynatrace-instance-name> -k <dynatrace-api-key> -g <activegate-instance> -m <sslchecker-plugin-module-id> -i <sslchecker-plugin-endpoint-id> -n <sslchecker-plugin-endpoint-name> -r <sslchecker-endpoint-enabled>


    Args:
      -d <dynatrace-instance-name>: Dynatrace instance name (e.g. yrk32651)
      -k <dynatrace-api-key>: Dynatrace api key
      -g <activegate-instance>: Active gate instance name (e.g. activegate-nonprod-vmss000001)
      -m <sslchecker-plugin-module-id>:   
      -i <sslchecker-plugin-endpoint-id>: SSL Checker plugin endpoint id
      -n <sslchecker-plugin-endpoint-name>
      -r <sslchecker-endpoint-enabled> [true|false]: check for endpoint enabled/disabled
    """
    dynatrace_instance_name=''
    dynatrace_api_key=''
    activegate_instance_name=''
    plugin_module_id=''
    plugin_endpoint_id=''
    plugin_endpoint_name=''
    endpoint_enabled=True

    try:
        opts, args = getopt.getopt(
            argv, "d:k:g:m:i:n:r", ["dynatrace_instance_name=", "dynatrace_api_key=", "activegate_instance_name=",
                                            "plugin_module_id=", "plugin_endpoint_id=", "plugin_endpoint_name=", "endpoint_enabled="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--dynatrace-instance"):
            dynatrace_instance_name = arg
        elif opt in ("-k", "--dynatrace-api-key"):
            dynatrace_api_key = arg
        elif opt in ("-g", "--activegate-instance"):
            activegate_instance_name = arg
        elif opt in ("-m", "--sslchecker-plugin-module-id"):
            plugin_module_id = arg
        elif opt in ("-i", "--sslchecker-plugin-endpoint-id"):
            plugin_endpoint_id = arg
        elif opt in ("-n", "--sslchecker-plugin-endpoint-name"):
            plugin_endpoint_name = arg
        elif opt in ("-r", "--sslchecker-endpoint-enabled"):
            endpoint_enabled = True

    if not dynatrace_api_key:
        dynatrace_api_key = os.environ["api_key"]

      

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
    base_url = "https://{}.live.dynatrace.com".format(dynatrace_instance_name)
    dynatrace_registration_method = "PUT"
    dynatrace_req_headers = {"Authorization": "Api-token {}".format(dynatrace_api_key)}
    dynatrace_req_headers["Content-Type"] = "application/json"
    print("***** alll values here: pluginEndpointId:{},**endpointname:{},**endpointEnabled:{},**base_url:{},**pluginModuleId:{},**ag_instance_name:{},**domainout:{},**domainin:{}"
    .format(plugin_endpoint_id,plugin_endpoint_name,endpoint_enabled,base_url,plugin_module_id,activegate_instance_name,csm_metrickeys_domainout,csm_metrickeys_domainin))
    dynatrace_registration_req_data = {"pluginId": plugin_endpoint_id, "name": plugin_endpoint_name, "enabled": endpoint_enabled,
                                        "properties": {"ClusterAddress": base_url,
                                                    "ExpirationDelta": "10", "DomainsToIgnore": "",
                                                    "ApiToken": "{}".format(dynatrace_api_key),"OutboundMetricNames":csm_metrickeys_domainout,"InboundMetricNames":csm_metrickeys_domainin},
                                        "activeGatePluginModule": {"id": plugin_module_id, "name": activegate_instance_name}}

    print("*** Before json dumps:{}".format(dynatrace_registration_req_data))
    dynatrace_registration_data = json.dumps(dynatrace_registration_req_data).encode("utf-8")
    dynatrace_registration_url = 'https://yrk32651.live.dynatrace.com/api/config/v1/plugins/custom.remote.python.sslCheck/endpoints/6691303106622817277'
    dynatrace_registration_req = url_request.Request(url=dynatrace_registration_url,
                                                    data=dynatrace_registration_data,
                                                    headers=dynatrace_req_headers, method=dynatrace_registration_method)
    print("Request:{}".format(dynatrace_registration_data))
    with url_request.urlopen(dynatrace_registration_req, timeout=120) as response:
        print("Plugin endpoint {} complete: status={}, reason={}".format(dynatrace_registration_method, response.status, response.reason))

if __name__ == "__main__":
    main(sys.argv[1:])
