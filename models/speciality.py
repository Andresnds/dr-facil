import mongoengine
from mongoengine import errors, fields

class Speciality(mongoengine.Document):

	name = fields.StringField(required=True, max_length=50)


	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
		}


	@classmethod
	def find_all(cls):
		try:
			return cls.objects
		except errors.DoesNotExist:

			return None
