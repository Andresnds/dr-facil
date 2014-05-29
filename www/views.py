from www import app
from flask import make_response, jsonify, request, abort
from models.user import Doctor, Patient
from models.specialty import Specialty

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(Doctor.get_all())


@app.route('/doctor', methods=['GET'])
def get_doctor():
    if not request.json or request.json.get('id') is None:
        abort(400)
    try:
        doctor = Doctor.find_by_id(request.json['id'])
    except:
        abort(500)
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


@app.route('/patient', methods=['GET'])
def get_patient():
    if not request.json or request.json.get('id') is None:
        abort(400)
    try:
        patient = Patient.find_by_id(request.json['id'])
    except:
        abort(500)
    return jsonify(patient.to_dict())

@app.route('/patient/by_email', methods=['GET'])
def get_patient_id():
    if not request.json or request.json.get('email') is None:
        abort(400)
    try:
        patient = Patient.find_by_email(request.json['email'])
    except:
        abort(500)
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

@app.route('/specialties')
def get_specialties():
    try:
        return jsonify(Specialty.get_all())
    except:
        abort(500)

@app.route('/specialties', methods=['POST'])
def insert_specialty():
    if not request.json:
        abort(400)
    try:
        specialty = Specialty(name=request.json['name'])
        specialty.save()
    except:
        abort(500)
    return jsonify(specialty.to_dict())

@app.route('/doctors/search')
def search_doctors():
    doctors = Doctor.get_all()['doctors']

    return jsonify(_filter_doctors(doctors, request.args))

def _filter_doctors(doctors, params):
    result = []
    for doctor in doctors:
        belongs = False
        for specialty in doctor['specialties']:
            if specialty['id'] in params.get('specialties').split(','):
                belongs = True
        if belongs:
            result.append(doctor)

    # doctors = result
    # result = []
    # for doctor in doctors:
    return {'result': result}

def _populate_doctor(params):
    doctor = Doctor(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
            specialties = [],
        )
    for specialty_id in params['specialties']:
        doctor.specialties.append(Specialty.find_by_id(specialty_id))
    return doctor

def _populate_patient(params):
    return Patient(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
        )
