class FileAttachment:
    """
    activity-service response for file attachments are a list of this object.
    only necessary fields are mapped here - this is not a comprehensive model object
    """
    def __init__(self, uuid:str, private_attachment: str, name: str, filepath: str):
        if not uuid or not private_attachment or not name or not filepath:
            raise Exception(f'missing required fields in FileAttachment for uuid: {str(uuid)}')

        self.uuid = uuid
        self.private_attachment = private_attachment
        self.name = name
        self.filepath = filepath

    #TODO - feels like im missing some fields.
    #TODO - probably dont need to bother with pydantic

class FileUploadEvent:
    data: list[dict[str, any]] = []