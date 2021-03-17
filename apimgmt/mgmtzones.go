package main
import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "os"
)
type Response struct {
    Name    string    `json:"name"`
    ManagementZone []ManagementZone `json:"values"`
}

// A Pokemon Struct to map every pokemon to.
type ManagementZone struct {
    ManagementZoneId string  `json:"id"`
    ManagementZoneName string `json:"name"`
}

func GetAllMgmtZones(endpointUrl string){
    client := http.Client{}
	req, err := http.NewRequest("GET", endpointUrl, nil)
	req.Header.Add("Authorization", "Api-Token I1RtfySETHGKBGasu0Q-e")
    resp, err := client.Do(req)

    if err != nil {
        fmt.Print(err.Error())
        os.Exit(1)
    }

    responseData, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        log.Fatal(err)
    }
    ParseJson(responseData)
}

func ParseJson(responseData []byte){
    var responseObject Response
    json.Unmarshal(responseData, &responseObject)

    fmt.Println(responseObject.Name)
    fmt.Println(len(responseObject.ManagementZone))

    for i := 0; i < len(responseObject.ManagementZone); i++ {
        fmt.Println("Management Zone Name",responseObject.ManagementZone[i].ManagementZoneName)
        fmt.Println("Management Zone Id",responseObject.ManagementZone[i].ManagementZoneId)
    }
}