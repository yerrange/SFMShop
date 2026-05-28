class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self.email

    @classmethod
    def create_object(cls, data):
        obj = cls(data[1], data[2])
        obj.id = data[0]
        return obj
