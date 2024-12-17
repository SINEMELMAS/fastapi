from fasthtml.common import *

app = FastHTML()

@app.route("/")
def index():
    return Div(P("Click me!", hx_get="/change"))

@app.route("/change")
def change_text():
    return P("You clicked the button!")

serve()