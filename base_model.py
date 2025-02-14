from peewee import Model


class BaseModel(Model):
    class Meta:
        database = None  # База данных будет установлена позже