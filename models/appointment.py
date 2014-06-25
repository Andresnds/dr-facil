import mongoengine
from mongoengine import errors, fields
from models.user import Professional, Patient

class Appointment(mongoengine.Document):

	id = fields.SequenceField(primary_key=True, sequence_name='appointment')
	professional = fields.ReferenceField(Professional, required=True)
	patient = fields.ReferenceField(Patient, required=True)
	start_date = fields.StringField(required=True)
	end_date = fields.StringField(required=True)

	def to_dict(self, professional_info=False, patient_info=False):
		return {
			'id': str(self.id),
			'professional_id': str(self.professional.id),
			'patient_id': str(self.patient.id),
			'start_date': self.start_date,
			'end_date': self.end_date,
		}

	@classmethod
	def find_by_professional(cls, professional):
		try:
			return cls.objects(professional=professional)
		except errors.DoesNotExist:
			return None

	@classmethod
	def find_by_patient(cls, patient):
		try:
			return cls.objects(patient=patient)
		except errors.DoesNotExist:
			return None
