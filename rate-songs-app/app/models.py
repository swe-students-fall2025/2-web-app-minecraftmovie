from flask_login import UserMixin

class UserDoc(UserMixin):
    def __init__(self, doc):
        self.doc = doc

    def get_id(self):
        return str(self.doc["_id"])

    @property
    def username(self):
        return self.doc.get("username") or (self.doc.get("email","").split("@")[0] if self.doc.get("email") else None)