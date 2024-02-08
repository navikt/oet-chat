import urllib.request
import json
import os
import ssl
import logging


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chat_med_endpoint(question: str, api_key: str, url, navn_på_endepunkt):
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
    except Exception as error:
        print("The request failed with status code: " )
        logger.info(f"{error}")
        logger.info("The request failed with status code: ")
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        return "Det funka ikke"
