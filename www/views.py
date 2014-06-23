from www import app
from flask import make_response, jsonify, request, abort
from models.user import Professional, Patient
from models.specialty import Specialty

@app.route('/professionals', methods=['GET'])
def get_professionals():
    return jsonify(Professional.get_all())


@app.route('/professional', methods=['GET'])
def get_professional():
    if not request.json or request.json.get('id') is None:
        abort(400)
    try:
        professional = Professional.find_by_id(request.json['id'])
    except:
        abort(500)
    return jsonify(professional.to_dict())


@app.route('/professionals', methods=['POST'])
def insert_professional():
    if not request.json:
        abort(400)
    try:
        professional = _populate_professional(request.json)
        professional.save()
    except:
        abort(500)
    return jsonify(professional.to_dict())


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

@app.route('/professionals/search')
def search_professionals():
    professionals = Professional.get_all()['professionals']

    return jsonify(_filter_professionals(professionals, request.args))

def _filter_professionals(professionals, params):
    result = []
    for professional in professionals:
        belongs = False
        for specialty in professional['specialties']:
            if specialty['id'] in params.get('specialties').split(','):
                belongs = True
        if belongs:
            result.append(professional)

    # professionals = result
    # result = []
    # for professional in professionals:
    return {'result': result}

def _populate_professional(params):
    professional = Professional(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
            specialties = [],
        )
    for specialty in params['specialties']:
        specialty_id = specialty['id']
        professional.specialties.append(Specialty.find_by_id(specialty_id))
    return professional

def _populate_patient(params):
    return Patient(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
        )
