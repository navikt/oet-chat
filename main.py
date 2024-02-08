import os
import time

from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from textwrap import dedent
from ml_ot_bot import chat_med_endpoint

api_key = 'W53UMisVecwVl8TkY4GwB1Ki15Wrmn8F'#os.environ["key"]
url = 'https://ot-ml-kategorisering-iterasjon1.swedencentral.inference.ml.azure.com/score'
#url = os.environ["URL_ENDEPUNKT"]

navn_på_endepunkt = 'ot-ml-kategorisering-iterasjon1'#os.environ["NAVN_ENDEPUNKT"]



def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("roed.png"), style={"float": "right", "height": 60}
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


def textbox(text, box="AI", name="OT ML"):
    text = text.replace(f":", "").replace("You", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("hg.png"),
            style={
                "border-radius": 50,
                "height": 35,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([thumbnail,textbox])

    else:
        raise ValueError("Incorrect option for `box`.")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)
controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Skriv noe", type="text"),
        dbc.Button("Submit", id="submit"),
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("OT-ML", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
    ],
)
@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]

@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return "Hei på deg"

@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    print(n_submit)
    if n_clicks == 0 and n_submit is None:
        print("Heiehie")
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    name = ""

    prompt = dedent(
        f"""
    """
    )

    # First add the user input to the chat history
    chat_history += f"You: {user_input}<split>{name}:"

    model_input = prompt + chat_history.replace("<split>", "\n")
    if "menneske" in user_input:
        time.sleep(8)
        model_output = """
        Hei, du snakker med et menneske, jeg heter Claude. Jeg er et skikkelig bra menneske og kan hjelpe deg på en bra
        måte, la oss finne ut av hva det er du lurer på. Kan du gjenta hva du lurer på? """
    else:
        model_output = chat_med_endpoint(user_input, api_key, url, navn_på_endepunkt)
        print(model_output)
    chat_history += f"{model_output}<split>"

    return chat_history, None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050, dev_tools_ui=False)
