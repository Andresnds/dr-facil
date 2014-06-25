import json, datetime, hashlib
import dateutil.parser as dateparser
from www import app
from flask import make_response, jsonify, request, abort
from models.user import Professional, Patient, Address
from models.specialty import Specialty
from models.insurance import Insurance
from models.appointment import Appointment

@app.route('/professionals', methods=['GET'])
def get_professionals():
    return json.dumps(Professional.get_all())


@app.route('/professional/<professional_id>', methods=['GET'])
def get_professional(professional_id):
    try:
        professional = Professional.find_by_id(professional_id)
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


@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = Patient.find_by_id(patient_id)
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

@app.route('/patient/appointments/<patient_id>')
def get_appointment_patient_id(patient_id):
    try:
        patient = Patient.find_by_id(patient_id)
        appointments = [appointment.to_dict() for appointment in Appointment.find_by_patient(patient)]
    except:
        abort(500)
    return json.dumps(appointments)

@app.route('/professional/appointments/<professional_id>')
def get_appointment_professional_id(professional_id):
    try:
        professional = Professional.find_by_id(professional_id)
        appointments = [appointment.to_dict() for appointment in Appointment.find_by_professional(professional)]
    except:
        abort(500)
    return json.dumps(appointments)

@app.route('/appointments', methods=['POST'])
def create_appointment():
    if not request.form:
        abort(400)
    # try:
        params = request.form
        professional = Professional.find_by_id(params['professional_id'])
        appointments = Appointment.find_by_professional(professional)
        start_date = dateparser.parse(params['start_date'])
        end_date = dateparser.parse(params['end_date'])
        for appointment in appointments:
            schedule_start_date = dateparser.parse(appointment.start_date)
            schedule_end_date = dateparser.parse(appointment.end_date)
            if not (start_date <= schedule_start_date and end_date <= schedule_start_date or start_date >= schedule_end_date and end_date >= schedule_end_date):
                abort(404)

        print params

        appointment = Appointment(
                professional = professional,
                patient = Patient.find_by_id(params['patient_id']),
                start_date = params['start_date'],
                end_date = params['end_date'],
            )

        print appointments

        appointment.save()
    # except Exception as e:
        # print e
        # abort(500)
    return jsonify(appointment.to_dict())

@app.route('/professional/slots/<professional_id>')
def get_slots(professional_id):
    try:
        professional = Professional.find_by_id(professional_id)
        appointments = Appointment.find_by_professional(professional)
        start_date = dateparser.parse(request.args['start_date'])
        end_date = dateparser.parse(request.args['end_date'])
        slots = _found_slots(start_date, end_date, professional_id)
    except:
        abort(500)
    return json.dumps(slots)

@app.route('/professionals/search')
def search_professionals():
    professionals = Professional.get_all()
    return json.dumps(_filter_professionals(professionals, request.args))

def _filter_professionals(professionals, params):
    result = professionals

    if params.get('specialty_ids') is not None:
        professionals = result
        result = []
        for professional in professionals:
            belongs = False
            for specialty in professional['specialties']:
                if specialty['id'] in params.get('specialty_ids').split(','):
                    belongs = True
                    break
            if belongs:
                result.append(professional)

    if params.get('insurance_ids') is not None:
        professionals = result
        result = []
        for professional in professionals:
            belongs = False
            for insurance in professional['insurances']:
                if insurance['id'] in params.get('insurance_ids').split(','):
                    belongs = True
                    break
            if belongs:
                result.append(professional)

    print result

    if params.get('start_date') is not None and params.get('end_date') is not None:
        professionals = result
        result = []
        for professional in professionals:
            start_date = dateparser.parse(params['start_date'])
            end_date = dateparser.parse(params['end_date'])
            print start_date
            print end_date
            if len(_found_slots(start_date, end_date, professional['id']))!= 0:
                result.append(professional)

    print result

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

def _found_slots(start_date, end_date, professional_id):
    start_date = start_date + datetime.timedelta(minutes=(30-start_date.minute%30)%30)
    slots = []
    half_hour = datetime.timedelta(minutes=30)
    professional = Professional.find_by_id(professional_id)
    appointments = Appointment.find_by_professional(professional)
    while start_date + half_hour <= end_date:
        occupied = False
        for appointment in appointments:
            schedule_start_date = dateparser.parse(appointment.start_date)
            schedule_end_date = dateparser.parse(appointment.end_date)
            if not (start_date <= schedule_start_date and start_date + half_hour <= schedule_start_date or start_date >= schedule_end_date and start_date + half_hour >= schedule_end_date):
                occupied = True
                break
        if not occupied:
            slots.append({
                    'id': hashlib.md5(str(start_date)+professional_id).hexdigest(),
                    'start_date': start_date.isoformat(),
                })
        start_date += half_hour
    return slots
