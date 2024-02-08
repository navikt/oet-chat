import urllib.request
import json
import os
import ssl


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


api_key = os.environ["api-key-azure-endepunkt"]["key"]
url = os.environ["URL_ENDEPUNKT"]
navn_på_endepunkt = os.environ["NAVN_ENDEPUNKT"]


def chat_med_endpoint(question):
    allowSelfSignedHttps(True)
    data = {'chat_input': question, 'chat_history': []}

    body = str.encode(json.dumps(data))

    # Replace this with the primary/secondary key or AMLToken for the endpoint
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key),
               'azureml-model-deployment': navn_på_endepunkt}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = json.loads(response.read().decode("utf-8"))
        return result["chat_output"]
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return ""


print(chat_med_endpoint("Hei, hva er lønn?"))
