class Reply(object):
    """{
        "kind": "drive#commentReply",
        "replyId": string,
        "createdDate": datetime,
        "modifiedDate": datetime,
        "author": {
            "kind": "drive#user",
            "displayName": string,
            "picture": {
                "url": string
            },
            "isAuthenticatedUser": boolean,
            "permissionId": string,
            "emailAddress": string
        },
        "htmlContent": string,
        "content": string,
        "deleted": boolean,
        "verb": string
    }"""

    def __init__(self, _reply):
        self._reply = _reply


class Comment(object):
    """{
        "kind": "drive#comment",
        "selfLink": string,
        "commentId": string,
        "createdDate": datetime,
        "modifiedDate": datetime,
        "author": {
            "kind": "drive#user",
            "displayName": string,
            "picture": {
                "url": string
            },
            "isAuthenticatedUser": boolean,
            "permissionId": string,
            "emailAddress": string
        },
        "htmlContent": string,
        "content": string,
        "deleted": boolean,
        "status": string,
        "context": {
            "type": string,
            "value": string
        },
        "anchor": string,
        "fileId": string,
        "fileTitle": string,
        "replies": [
            replies Resource
        ]
    }"""

    def __init__(self, _comment):
        self._comment = _comment

    @property
    def text(self):
        return self._comment.get("content")

    @property
    def status(self):
        return self._comment.get("status")

    @property
    def author(self):
        return self._comment["author"].get("displayName")

    @property
    def link(self):
        return self._comment.get("selfLink")

    @property
    def replies(self):
        return [Reply(obj) for obj in self._comment.get("replies", []) if not obj.get("deleted")]
