import urllib.request
import json
import os
import ssl
import logging

import numpy as np

liste_med_eg_veit_ikkje_svar = ["Eg veit ikkje", "Eg kan ikkje svare på det", "Eg kan ikkje hjelpe deg med det",
                                "Eg treng meir informasjon for å hjelpe deg", "Eg kan ikkje svare på det spørsmålet",
                                "Nå forstår eg deg ikkje", "Dette var eit dumt spørsmål, eg kan ikkje svare på det"]
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_history = []
chat_history1 = [{"inputs":
                              {"chat_input": "Jeg får 10.000kr i lønn, hva er det for noe?"},
                          "outputs":
                              {
                                  "chat_output": "Lønn er betalinga ein person får for arbeidet sitt. Spørsmål om eiga lønn skal "
                                                 "alltid rettast til leiar. Lønna blir utbetalt den 12. kvar månad. Lønna vert "
                                                 "utbetalt som etterbetaling og forskudd den 12. kvar månad. Feriepengar blir "
                                                 "utbetalt i juni. Du får 10.000 kr i lønn. "}
                          },
                         {"inputs":
                             {
                                 "chat_input": "Kan du gjenta hvor mye jeg får i lønn, jeg jobber 10 timer i uka? "},
                             "outputs":
                                 {
                                     "chat_output": "Du får 10.000 kr i lønn. (Source: User input)"}
                         }
                         ]

def chat_med_endpoint(question: str, api_key: str, url, navn_på_endepunkt):
    allowSelfSignedHttps(True)
    data = {'chat_input': question, 'chat_history': chat_history[:-5]}

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
        result = json.loads(response.read().decode("utf-8"))["chat_output"]
        chat_history.append({"inputs":
                                 {"chat_input": question},
                                  "outputs":
                                      {
                                          "chat_output": result}
                                  })
        if result == 'Eg treng meir informasjon for å hjelpe deg':
            return np.random.choice(liste_med_eg_veit_ikkje_svar)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        return "Jeg kan ikke hjelpe deg. Prøv igjen senere :)"
