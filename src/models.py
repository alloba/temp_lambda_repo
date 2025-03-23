from pydantic import BaseModel

class FileAttachment(BaseModel):
    """
    activity-service response for file attachments are a list of this object.
    only necessary fields are mapped here - this is not a comprehensive model object
    """
    privateAttachment: str
    name: str
    filePath: str

    #TODO - feels like im missing some fields.
    #TODO - probably dont need to bother with pydantic

class FileUploadEvent:
    data: list[dict[str, any]] = []