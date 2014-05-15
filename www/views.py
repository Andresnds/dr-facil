from www import app
from flask import make_response, jsonify, request, abort
from models.user import Doctor, Patient

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(Doctor.get_all())


@app.route('/doctor/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = Doctor.find_by_id(doctor_id)
    return jsonify(doctor.to_dict())


@app.route('/doctors', methods=['POST'])
def insert_doctor():
    if not request.json:
        abort(400)
    try:
        doctor = _populate_doctor(request.json)
        doctor.save()
    except:
        abort(500)        
    return jsonify(doctor.to_dict())


@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.find_by_id(patient_id)
    return jsonify(patient.to_dict())


@app.route('/patients', methods=['POST'])
def insert_patient():
    if not request.json:
        abort(400)
    try:
        patient = _populate_patient(request.json)
        patient.save()
    except:
        abort(500)        
    return jsonify(patient.to_dict())

def _populate_doctor(params):
    return Doctor(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
            specialities = params['specialities'],
        )

def _populate_patient(params):
    return Patient(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
        )
