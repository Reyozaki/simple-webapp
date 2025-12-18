import io

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

env = Environment(loader=FileSystemLoader("templates"))


async def render_pdf(template_name: str, context: dict) -> bytes:
    template = env.get_template(template_name)
    html_content = template.render(context)

    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)

    return pdf_io.getvalue()
