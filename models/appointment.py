import mongoengine
from mongoengine import errors, fields
from models.user import Professional, Patient
from models.clinic import Clinic


class Schedule(mongoengine.EmbeddedDocument):
	
	begin = fields.DateTimeField(required=True)
	end = fields.DateTimeField(required=True)

	def to_dict(self):
		return {
			'begin': self.begin,
			'end': self.end,
		}


class Appointment(mongoengine.Document):
	
	professional = fields.ReferenceField(Professional, required=True)
	patient = fields.ReferenceField(Patient, required=True)
	schedule = fields.EmbeddedDocumentField(Schedule, required=True)
	clinic = fields.ReferenceField(Clinic, required=True)

	def to_dict(self, professional_info=False, patient_info=False):
		result = {
			'schedule': self.schedule.to_dict(),
			'clinic': self.clinic.to_dict(),
		}

		if professional_info:
			result['professional'] = self.professional.to_dict()
		if patient_info:
			result['patient'] = self.patient.to_dict()

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
