import mongoengine, bson
from specialty import Specialty
from mongoengine import errors, fields

class User(mongoengine.Document):

    meta = {'allow_inheritance': True}

    username = fields.StringField(required=True, max_length=20)
    email = fields.StringField(required=True)
    first_name = fields.StringField(required=True, max_length=50)
    last_name = fields.StringField(required=True, max_length=50)
    birthdate = fields.StringField(required=True)
    #look at the DateTimeField Documentation later
    gender = fields.StringField(required=True, max_length=6)

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': self.birthdate,
            'gender': self.gender,
        }

    def get_role(self):
        raise NotImplementedError()

    @classmethod
    def find_by_id(cls, user_id):
        oid = bson.objectid.ObjectId(user_id)
        try:
            return cls.objects.get(id=oid)
        except errors.DoesNotExist:
            return None

    @classmethod
    def find_by_username(cls, username):
        try:
            return cls.objects.get(username=username)
        except errors.DoesNotExist:
            return None

    @classmethod
    def find_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except errors.DoesNotExist:
            return None

class Professional(User):

    specialties = fields.ListField(fields.ReferenceField(Specialty, required=True), required=True)

    def to_dict(self):
        result = super(Professional, self).to_dict()
        result['specialties'] = []
        for specialty in self.specialties:
            result['specialties'].append(specialty.to_dict())
        return result

    def get_role(self):
        return 'professional'

    @classmethod
    def get_all(cls):
        result = []
        for professional in cls.objects:
            result.append(professional.to_dict())
        return {'professionals': result}


class Patient(User):

    def get_role():
        return 'patient'
