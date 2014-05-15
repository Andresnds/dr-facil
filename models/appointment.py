import mongoengine
from mongoengine import errors, fields
from models.user import Doctor, Patient

class Appointment(mongoengine.Document):
	
	doctor = fields.ReferenceField(Doctor, required=True)
	patient = fields.ReferenceField(Patient, required=True)
	schedule = fields.ReferenceField(Schedule, required=True)
	clinic = fields.ReferenceField(Clinic, required=True)

	def to_dict(self, doctor_info=False, patient_info=False):
		result = {
			'schedule': self.schedule.to_dict(),
			'clinic': self.clinic.to_dict(),
		}

		if doctor_info:
			result['doctor'] = self.doctor.to_dict()
		if patient_info:
			result['patient'] = self.patient.to_dict()

		return result

	@classmethod
	def find_by_doctor(cls, doctor):
		try:
			return cls.objects.get(doctor=doctor)
		except errors.DoesNotExist:
			return None

	@classmethod
	def find_by_patient(cls, patient):
		try:
			return cls.objects.get(patient=patient)
		except errors.DoesNotExist:
			return None			


class Schedule(mongoengine.EmbeddedDocument):
	
	begin = fields.DateTimeField(required=True)
	end = fields.DateTimeField(required=True)

	def to_dict(self):
		return {
			'begin': self.begin,
			'end': self.end,
		}