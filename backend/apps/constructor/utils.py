from ..documents.models import DocumentSection


def get_section_values(section: DocumentSection) -> dict:
    """
    Get the values of a section
    """
    values = {
        "title": section.title,
    }

    if section.type == "section-article":
        values["description"] = section.description
        values["unitPriceHT"] = section.unit_price_ht
        values["quantity"] = section.quantity
        values["vatRate"] = section.vat_rate
        values["articleType"] = section.article_type
        values["discount"] = section.discount
        values["discountType"] = section.discount_type
        values["discountDescription"] = section.discount_description
        values["unit"] = section.unit
        values["displayPriceInfos"] = section.display_price_infos

    elif section.type == "section-subtotal":
        values["subtotal"] = section.subtotal

    return values
