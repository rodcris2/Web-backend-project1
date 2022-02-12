import http.server
import socketserver
import http.client
import json
import urllib.parse

PORT = 8080
purgoAPI = 'www.purgomalum.com'
foassAPI = 'www.foaas.com'

def redactMessageJSON(args):
    foasssConnect = http.client.HTTPSConnection(foassAPI)
    foasssheader = {"Accept" : "application/json"} # adds the key and value to the path
    foasssConnect.request("GET", args, headers=foasssheader) 
    foasssResponse = foasssConnect.getresponse() 
    foassJSON = json.loads(foasssResponse.read()) # retrieve data from foassAPI
    foassMessage = urllib.parse.quote(foassJSON["message"])

    purgoConnect = http.client.HTTPSConnection(purgoAPI) 
    purgoConnect.request("GET", f'/service/json?text={foassMessage}') # request sent to server to use the service to filter the JSON output retrieved
    purgoResponse = purgoConnect.getresponse() 
    purgoJSON = json.loads(purgoResponse.read()) # retrieve data from purogAPI

    foassJSON["message"] = purgoJSON["result"] # purgoJSON message compares to foassJSON message and writes over the foassJSON any part of the message that is not similar

    purgoConnect.close()
    foasssConnect.close()
    return foassJSON

class serverHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        payload = '<span>Usage: http://localhost:8080 +  <a href="https://foaas.com/">foass command</a></span>' # Displays how to properly name the address in order to connect to the server
        if self.path != '/' and self.path != '/favicon.ico':
            data = redactMessageJSON(self.path) # copies the path that the user entered to use in the function
            message = data["message"] # retrieves the JSON message found in that path
            signature = data["subtitle"] # retrieves the JSON subtitle found in that path

            divStyle='padding:60px;margin-bottom:30px;font-size:18px;font-weight:200;line-height:30px;color:inherit;background-color:#eee;-webkit-border-radius:6px;-moz-border-radius:6px;border-radius:6px'
            h1Style='margin-bottom:0;font-size:60px;line-height:1;color:inherit;letter-spacing:-1px'
            payload = f'<div style={divStyle}><h1 style={h1Style}>{message}</h1><p><em>{signature}</em></p></div>' # Displays the message and signature retrieved and displays it in a HTML format
            payload += '<center><a style="text-decoration: none; color:baby-blue;" href="https://foaas.com/">foass.com</a>' # Dispalyes the foass.com website

        self.wfile.write(payload.encode('utf-8'))


with socketserver.TCPServer(("", PORT), serverHTTPRequestHandler) as httpd: # creates a server so user would be able to use the address
    print("serving at port", PORT)
    httpd.serve_forever()
