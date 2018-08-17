import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True) #if set to True this method will fail silently and return False.

    print("Request:")
    print(json.dumps(req, indent=2)) #convert them to JSON data and then print it (python data to Json)
    #  the json data will be indented

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "detail_po":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    NAME = parameters.get("PO_number")

    BANK = {'123':'PO_Approved', '234':'PO Rejected', '345':'Sent to Approval List'}

    speech = "PO Status " + NAME + " is " + str(BANK[NAME]) + " Thank You !."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "POAgentDetails"
    }

@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this is a static reply from webhook"
    my_result = {
    "speech" :speech,
    "displaytext" :speech,
    "source" : "POAgentDetails"

}

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print("Starting app on port %d" % (port))

    app.run( debug=True, port=port, host='0.0.0.0')
