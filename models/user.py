import mongoengine
from mongoengine import errors, fields

class User(mongoengine.Document):

    meta = {'allow_inheritance': True}

    username = fields.StringField(required=True, max_length=20)
    email = fields.StringField(required=True)
    first_name = fields.StringField(max_length=50)
    surname = fields.StringField(max_length=50)
    birthdate = fields.DateTimeField()
    gender = fields.StringField(max_length=6)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': str(self.birthdate),
            'gender': self.gender,
        }

    def get_role(self):
        raise NotImplementedError()

    @classmethod        
    def find_by_id(cls, user_id):
        try:
            return cls.objects.get(id=user_id)
        except errors.DoesNotExist:
            return None

    @classmethod        
    def find_by_username(cls, username):
        try:
            return cls.objects.get(username=username)
        except errors.DoesNotExist:
            return None

class Doctor(User):
    
    specialities = fields.ListField(fields.StringField(max_length=50), required=True)

    def to_dict(self):
        result = super(Doctor, self).to_dict()
        result['specialities'] = self.specialities
        return result

    def get_role(self):
        return 'doctor'

class Patient(User):

    def get_role():
        return 'patient'
        