import sys
import http.client
import json
import urllib.parse

purgoAPI = 'www.purgomalum.com'
foassAPI = 'www.foaas.com'

if not sys.argv[1:]:
    print("Usage: redact URL")
else:
    # print(sys.argv[1])
    # foass API
    foasssConnect = http.client.HTTPSConnection(foassAPI)
    foasssheader = {"Accept" : "application/json"} # adds the key and value to the path
    foasssConnect.request("GET", sys.argv[1], headers=foasssheader) 
    foasssResponse = foasssConnect.getresponse() 
    foassJSON = json.loads(foasssResponse.read()) # retrieve data from foassAPI
    # print(foassJSON["message"])
    foassMessage = urllib.parse.quote(foassJSON["message"]) 

    # PurgoMalum API
    purgoConnect = http.client.HTTPSConnection(purgoAPI) 
    purgoConnect.request("GET", f'/service/json?text={foassMessage}') # request sent to server to use the service to filter the JSON output retrieved
    purgoResponse = purgoConnect.getresponse() 
    purgoJSON = json.loads(purgoResponse.read()) # retrieve data from purogAPI
    # print(r02["result"])

    foassJSON["message"] = purgoJSON["result"] # purgoJSON message compares to foassJSON message and writes over the foassJSON any part of the message that is not similar
    data = json.dumps(foassJSON, indent="\t") # sends data from python to JSON
    print(data) # display filtered result

    purgoConnect.close()
    foasssConnect.close()
