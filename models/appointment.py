import mongoengine
from mongoengine import errors, fields
from models.user import Professional, Patient

class Appointment(mongoengine.Document):

	professional = fields.ReferenceField(Professional, required=True)
	patient = fields.ReferenceField(Patient, required=True)
	start_date = fields.StringField(required=True)
	end_date = fields.StringField(required=True)

	def to_dict(self, professional_info=False, patient_info=False):

		if professional_info:
			result['professional'] = self.professional.to_dict()
		if patient_info:
			result['patient'] = self.patient.to_dict()

		result['start_date'] = self.start_date
		result['end_date'] = self.end_date

		return result

	@classmethod
	def find_by_professional(cls, professional):
		try:
			return cls.objects.get(professional=professional)
		except errors.DoesNotExist:
			return None

	@classmethod
	def find_by_patient(cls, patient):
		try:
			return cls.objects.get(patient=patient)
		except errors.DoesNotExist:
			return None
