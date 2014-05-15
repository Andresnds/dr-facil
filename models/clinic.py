import mongoengine
from mongoengine import errors, fields

class Clinic(mongoengine.Document):
	
	name = fields.StringField(required=True, max_length=50)
	address = fields.ReferenceField(Address, required=True)

	def to_dict(self):
		return {
			'name': self.name,
			'address': self.address.to_dict(),
		}

class Address(mongoengine.EmbeddedDocument):
	
	street = fields.StringField(required=True, max_length=50)
	number = fields.IntField()
	complement = fields.StringField(max_length=50)
	neighborhood = fields.StringField(required=True, max_length=50)
	city = fields.StringField(required=True, max_length=50)
	state = fields.StringField(required=True, max_length=50)
	country = fields.StringField(required=True, max_length=50)

	def to_dict(self):
		return {
			'street': self.street,
			'number': str(self.number) if self.number is not None else 's/n',
			'complement': self.complement,
			'neighborhood': self.neighborhood,
			'city': self.city,
			'state': self.state,
			'country': self.country,
		}
