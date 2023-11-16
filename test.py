#%%
import openai
import getpass
#%%
openai.api_key = getpass.getpass()

openai.api_base =  'https://faggruppe-gpt.openai.azure.com/' 
openai.api_type = 'azure' # Necessary for using the OpenAI library with Azure OpenAI
openai.api_version = '2023-08-01-preview' # Latest / target version of the API

deployment_name = 'gpt-4' # SDK calls this "engine", but naming
                                           # it "deployment_name" for clarity

#%%
prompt = 'What is Azure OpenAI?'
response = openai.Completion.create(engine=deployment_name, prompt=prompt)

print(response.choices[0].text)
#%%

def ask_gpt(query):

   
    gpt_instructions = """System: Follow these three instructions: 
        System: 1. Tell a joke,
        System: 3. Stick to Norwegian.   
        """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
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
