def generate_next_client_number(entreprise):
    """
    Generate the next client number
    """
    identifier = "C-"

    if entreprise.clients.count() == 0:
        return identifier + "000001"

    last_client = entreprise.clients.last()
    new_client_number = int(last_client.client_number.replace(identifier, "")) + 1

    return identifier + str(new_client_number).zfill(6)
