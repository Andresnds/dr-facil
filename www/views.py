import json
import dateutil.parser as dateparser
from www import app
from flask import make_response, jsonify, request, abort
from models.user import Professional, Patient, Address
from models.specialty import Specialty
from models.insurance import Insurance
from models.appointment import Appointment, Schedule

@app.route('/professionals', methods=['GET'])
def get_professionals():
    return json.dumps(Professional.get_all())


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
        same_patient = filter(lambda p: p["email"] is patient.email, Patient.get_all())
        if len(same_patient) is not 0:
            patient.save()

    except:
        abort(500)
    return jsonify(patient.to_dict())

@app.route('/specialties')
def get_specialties():
    try:
        return json.dumps(Specialty.get_all())
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

@app.route('/insurances')
def get_insurances():
    try:
        return json.dumps(Insurance.get_all())
    except:
        abort(500)

@app.route('/insurances', methods=['POST'])
def insert_insurance():
    if not request.json:
        abort(400)
    try:
        insurance = Insurance(name=request.json['name'])
        insurance.save()
    except:
        abort(500)
    return jsonify(insurance.to_dict())

@app.route('/appointments/by_patient')
def get_appointment_patient_id():
    if not request.json or request.json.get('patient_id') is None:
        abort(400)
    try:
        patient = Patient.find_by_id(request.json['patient_id'])
        appointments = [appointment.to_dict() for appointment in Appointment.find_by_patient(patient)]

    except:
        abort(500)
    return json.dumps(appointments)

@app.route('/appointments/by_professional')
def get_appointment_professional_id():
    if not request.json or request.json.get('professional_id') is None:
        abort(400)
    try:
        professional = professional.find_by_id(request.json['professional_id'])
        appointments = [appointment.to_dict() for appointment in Appointment.find_by_professional(professional)]
    except:
        abort(500)
    return json.dumps(appointments)

@app.route('/appointments', methods=['POST'])
def create_appointment():
    if not request.json:
        abort(400)
    try:
        params = request.json
        professional = Professional.find_by_id(params['professional_id'])
        appointments = Appointment.find_by_professional(professional)
        begin = dateparser(params['begin'])
        end = dateparser(params['end'])
        for appointment in appointments:
            schedule_begin = dateparser(appointment.schedule.begin)
            schedule_end = dateparser(appointment.schedule.end)
            if not (begin < schedule_begin and end < schedule_begin or begin > schedule_end and end > schedule_end):
                abort(404)

        schedule = Schedule(
                begin = params['begin'],
                end = params['end'],
            )
        appointment = Appointment(
                professional = professional,
                patient = Patient.find_by_id(params['patient_id']),
                schedule = schedule,
            )
        appointment.save()
    except:
        abort(500)
    return jsonify(appointment.to_dict())


@app.route('/professionals/search')
def search_professionals():
    professionals = Professional.get_all()
    return json.dumps(_filter_professionals(professionals, request.args))

def _filter_professionals(professionals, params):
    if params.get('specialties') is None:
        return professionals

    result = []
    for professional in professionals:
        belongs = False
        for specialty in professional['specialties']:
            if specialty['id'] in params.get('specialties').split(','):
                belongs = True
        if belongs:
            result.append(professional)

    professionals = result
    result = []
    for professional in professionals:
        belongs = False
        for insurance in professional['insurances']:
            if insurance['id'] in params.get('insurances').split(','):
                belongs = True
        if belongs:
            result.append(professional)

    return result

def _populate_professional(params):
    addrezz = params['address']
    professional = Professional(
            username = params['username'],
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            birthdate = params['birthdate'],
            gender = params['gender'],
            specialties = [],
            rating = params ['rating'],
            address = Address(
                    street = addrezz['street'],
                    number = addrezz.get('number'),
                    complement = addrezz.get('complement'),
                    neighborhood = addrezz['neighborhood'],
                    city = addrezz['city'],
                    state = addrezz['state'],
                    country = addrezz['country'],
                    zip_code = addrezz['zip_code'],
                ),
        )
    professional.image_url = params.get('image_url')
    for specialty in params['specialties']:
        specialty_id = specialty['id']
        professional.specialties.append(Specialty.find_by_id(specialty_id))
    for insurance in params['insurances']:
        insurance_id = insurance['id']
        professional.specialties.append(Insurance.find_by_id(insurance_id))
    return professional

def _populate_patient(params):
    patient = Patient(
            email = params['email'],
            first_name  = params['first_name'],
            last_name = params['last_name'],
            gender = params['gender'],
        )

    patient.birthdate = params.get('birthdate')

    patient.username = params.get('username')
    if patient.username is None:
        email = params.get('email')
        patient.username = email[0:email.find("@")]

    return patient
