from server.controller.schemas.entity import EntityDBSchema


class UserDBSchema(EntityDBSchema):
    email: str
    password: str

    class Config:
        from_attributes = True
