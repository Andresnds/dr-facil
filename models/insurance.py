import mongoengine, bson
from mongoengine import errors, fields

class Insurance(mongoengine.Document):

	name = fields.StringField(required=True, max_length=50)

	def to_dict(self):
		return {
			'id': str(self.id),
			'name': self.name,
		}

	@classmethod
	def get_all(cls):
		result = []
		for insurance in cls.objects:
			result.append(insurance.to_dict())
		return result

	@classmethod
	def find_by_id(cls, insurance_id):
		oid = bson.objectid.ObjectId(insurance_id)
		try:
			return cls.objects.get(id=oid)
		except errors.DoesNotExist:
			return None
