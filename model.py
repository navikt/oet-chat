# %%
import openai
import getpass

# %%
openai.api_key = getpass.getpass()

# %%
openai.api_base = 'https://faggruppe-gpt.openai.azure.com/'
openai.api_type = 'azure'  # Necessary for using the OpenAI library with Azure OpenAI
openai.api_version = '2023-08-01-preview'  # Latest / target version of the API

deployment_name = 'gpt-4'  # SDK calls this "engine", but naming



# %%
def ask_gpt(query, system_content, assistant_content):

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": query},
        ],
    )
    response_message = response["choices"][0]["message"]

    return response_message.content
