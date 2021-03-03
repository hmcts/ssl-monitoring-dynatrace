package main

import (
)

func main() {
    GetAllMgmtZones("non-prod",GetEndpointURL("non-prod","managementZones"))
}


func GetEndpointURL(env string,endpointname string) string{
   //var API_VERSION = "v1"
    //var ENV = ""
    var endpointURL = ""
    var baseURL string = ".live.dynatrace.com/api/config/v1"
    if (env== "non-prod"){
        endpointURL = "https://yrk32651"+baseURL+endpointname
    }
    return endpointURL
}