import data.oapen as OapenAPI


class OapenItem:
    def __init__(self, uuid, name, handle, expand, link, metadata):
        self.uuid = uuid
        self.name = name
        self.handle = handle
        self.expand = expand
        self.link = link
        self.metadata = metadata
        self.bitstreams = OapenAPI.get_bitstreams(self.uuid)

    def get_text_bitstream(self, limit=None):
        for bitstream in self.bitstreams:
            if bitstream["mimeType"] == "text/plain":
                retrieveLink = bitstream["retrieveLink"]
                text = str(OapenAPI.get(retrieveLink).decode("utf-8"))
                return text if limit is None else text[:limit]
        return ""


OapenSuggestion = (str, int)


def transform_item_data(data) -> OapenItem:
    uuid = data["uuid"]
    name = data["name"]
    handle = data["handle"]
    expand = data["expand"]
    link = data["link"]
    metadata = data["metadata"]

    return OapenItem(uuid, name, handle, expand, link, metadata)
