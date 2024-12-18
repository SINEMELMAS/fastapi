from fasthtml.common import *

app, rt = fast_app(live=True)


@rt('/')
def get():
    return Div(
        H1('Hello Nova this is H1'),
        H2('Hello Nova this is H2 '),
        H3('Hello Nova this is H3'),
        H4('Hello Nova this is H4'),
        H5('Hello Nova this is H5'),
        H6('Hello Nova this is H6'),

    )


serve()