import utils.general


def convert_to_csv(data: list[dict]) -> str:
    """Return a csv string with the graph data

    Returns:
        str: csv string
    """

    # create csv string
    csv_string = ""
    for item in data:
        flat_item = utils.general.flatten_dict(item)

        # create header if not already
        if csv_string == "":
            headers = list(flat_item.keys())
            csv_string += ",".join(headers) + "\n"
        # append data to csv string
        csv_string += ",".join([str(x) for x in flat_item.values()]) + "\n"

    # return csv string
    return csv_string
