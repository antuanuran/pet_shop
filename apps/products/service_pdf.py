import datetime
import io
import os

import weasyprint
from django.http import HttpRequest
from django.template import RequestContext, Template

CURRENT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")


def generate_pdf(order, user) -> bytes | bytearray | io.BytesIO:
    # render template
    with open(os.path.join(TEMPLATE_DIR, "cheque.html"), "r") as fd:
        template = Template(fd.read())
    context = RequestContext(
        HttpRequest(),
        {"user_name": user.email, "order_name": order.id, "date": datetime.date.today()},
    )
    html_out = template.render(context)
    html = weasyprint.HTML(string=html_out)

    # convert it to bytestream
    bstream = io.BytesIO()
    html.write_pdf(bstream)
    bstream.seek(0)
    return bstream
