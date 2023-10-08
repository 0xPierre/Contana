import sys
import os
from typing import List

import pdfkit

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contana.settings")
    sys.path.append("../../")

import django

django.setup()
from django.template import Template, Context
from apps.documents.models import Document, DocumentSection
from apps.entreprise.models import Entreprise


def construct_pdf(
    document: Document,
    sections: List[DocumentSection],
    entreprise: Entreprise,
    preview: bool = False,
) -> bytes:
    """
    Construct a pdf file from a document
    :param document: Document model
    :param sections: List of sections
    :param entreprise: Entreprise model
    :param preview: If the pdf is a preview or not and need to by
    :return: Bytes of the pdf file
    """
    # Change the working directory. This is needed because this service is called from differents places
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Open the template file
    with open("templates/template-white-dark.html", "r", encoding="utf8") as f:
        template_string = f.read()

    template = Template(template_string)
    context = Context(
        {
            "document": document,
            "client": document.client,
            "sections": sections,
            "entreprise": entreprise,
            "preview": preview,
        }
    )
    rendered_template = template.render(context)

    pdf_filename = "documents_ouput/out.pdf"
    pdfkit.from_string(
        rendered_template,
        "documents_ouput/out.pdf",
        options={
            "--page-size": "A4",
            "--margin-top": "0",
            "--margin-right": "0",
            "--margin-bottom": "8",
            "--margin-left": "0",
            "--encoding": "UTF-8",
            "enable-local-file-access": "",
            "--footer-right": "[page]/[topage]   ",
            # "--quiet": "",
        },
    )

    # read pdfbytes
    with open(pdf_filename, "rb") as f:
        pdf_bytes = f.read()

    # delete pdf file
    os.remove(pdf_filename)

    return pdf_bytes


if __name__ == "__main__":
    doc = Document.objects.last()
    construct_pdf(doc, doc.sections.all(), Entreprise.objects.last(), True)
