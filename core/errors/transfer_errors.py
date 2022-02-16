from werkzeug.exceptions import HTTPException

class TransferError(HTTPException):
    code=455