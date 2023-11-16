#%%
import os
import openai
import getpass
#%%
openai.api_key = getpass.getpass()

#%%
openai.api_base =  'https://faggruppe-gpt.openai.azure.com/' 
openai.api_type = 'azure' # Necessary for using the OpenAI library with Azure OpenAI
openai.api_version = '2023-08-01-preview' # Latest / target version of the API

deployment_name = 'gpt-4' # SDK calls this "engine", but naming
                                           # it "deployment_name" for clarity
#%%
response = openai.ChatCompletion.create(
    engine="gpt-4", # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Tell a joke"}
    ]
)
#%%
print(response['choices'][0]['message']['content'])
#%%
def ask_gpt(query):

   
    gpt_instructions = """System: Follow these three instructions: 
        System: 1. Tell a joke,
        System: 3. Stick to New Norwegian.   
        """

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[
            {"role": "system", "content": gpt_instructions},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": query},
        ],
    )
    response_message = response["choices"][0]["message"]

    return response_message.content



#%%
ask_gpt("si noe gøy")

# %%
