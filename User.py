from flask_login import UserMixin

users = {
    "test@example.com": {"password": "test123"},
    "a": {"password": "a"}
}
class User(UserMixin):
    def __init__(self, email, password):
        self.id = email
        self.password = password


    @staticmethod
    def get(user_id):
        user = users.get(user_id)
        if user:
            return User(user_id, user["password"])
        return None
