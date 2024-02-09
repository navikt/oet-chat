
import os
import time
import logging


from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from textwrap import dedent
from ml_ot_bot import chat_med_endpoint


api_key = os.environ["api_key"]



#url = 'https://ot-ml-kategorisering-iterasjon1.swedencentral.inference.ml.azure.com/score'
url = os.environ["URL_ENDEPUNKT"]

#navn_på_endepunkt = 'ot-ml-kategorisering-iterasjon1'
navn_på_endepunkt = os.environ["NAVN_ENDEPUNKT"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            src=app.get_asset_url("emne.png"),
            style={
                "border-radius": 50,
                "height": 85,
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
        textbox(x, box="user") if i % 2 != 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]

@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    time.sleep(1)
    return ""

@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks is None and n_submit is None:
        chat_history = f"""Hei! Jeg kan hjelpe deg som medarbeider i NAV med å svare på spørsmål som handler om å jobbe i NAV.
        Jeg lagrer alle spørsmål du stiller til meg slik at jeg kan lære av det. 
        Dersom du chatter med meg samtykker du til dette. 

        Hva kan jeg hjelpe deg med? 
          <split> :"""
                     
        return chat_history, None

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
    elif "fridtjof" in user_input:
        time.sleep(3)
        model_output = "Fridtjof er en kul fyr, han er en av de beste jeg vet om. Han er en skikkelig kul fyr"
    elif "wilhelm" in user_input:
        time.sleep(2)
        model_output = "Wilhelm er .... hva skal jeg si, han er en skikkelig kul fyr"
    elif "aurora" in user_input.lower():
        time.sleep(9)
        model_output = "Aurora er en skikkelig rar fyr, hun er en av de beste jeg vet om. Hun er en skikkelig kul fyr"
    elif "lars" in user_input.lower():
        time.sleep(1)
        model_output = "Lars er ekstremt kul, han er en av de beste jeg vet om. Han er en skikkelig kul fyr"
    else:
        model_output = chat_med_endpoint(user_input, api_key, url, navn_på_endepunkt)
        logger.info(f"Model input:{user_input}\nModel output: {model_output}")
    chat_history += f"{model_output}<split>"

    return chat_history, None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050, dev_tools_ui=False)

# %%
