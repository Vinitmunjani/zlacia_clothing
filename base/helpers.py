import os
import pdfkit
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings  # Import Django settings
import uuid

def save_pdf(params: dict):
    template = get_template("helpers/invoice.html")
    html = template.render(params)
    file_name = uuid.uuid4()
    # Specify options for wkhtmltopdf
    options = {
        'quiet': '',
        'page-size': 'A4',
    }

    # Specify the path to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # Replace with the actual path

    # Convert HTML to PDF using pdfkit
    pdf_data = pdfkit.from_string(html, False, options=options, configuration=config)

    # Save the PDF to the static directory
 
    pdf_path = os.path.join(settings.BASE_DIR,'static', 'invoices', f'{file_name}.pdf')  # Assumes 'invoices' directory exists

    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf_data)

    return pdf_path


