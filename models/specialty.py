import mongoengine, bson
from mongoengine import errors, fields

class Specialty(mongoengine.Document):

	name = fields.StringField(required=True, max_length=50)

	def to_dict(self):
		return {
			'id': str(self.id),
			'name': self.name,
		}

	@classmethod
	def get_all(cls):
		result = []
		for specialty in cls.objects:
			result.append(specialty.to_dict())
		return {'specialties': result}

	@classmethod
	def find_by_id(cls, specialty_id):
		oid = bson.objectid.ObjectId(specialty_id)
		try:
			return cls.objects.get(id=oid)
		except errors.DoesNotExist:
			return None
