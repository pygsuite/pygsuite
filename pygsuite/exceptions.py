from googleapiclient.errors import HttpError


class FatalHttpError(HttpError):
    pass


class FatalApiException(Exception):
    pass
