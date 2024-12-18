from fasthtml.common import *

app = FastHTML()

@app.route("/")
def index():
    return Html(
        Body(
            Form(
                Input(type="text", name="name"),
                Button("Submit", hx_post="/submit")
            ),
            Div(id="response")
        )
    )

@app.route("/submit", methods=["POST"])
def submit(name):
    return Div(f"Hello, {name}!")

serve()