# If you want to keep structure, define a "User" model here
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
