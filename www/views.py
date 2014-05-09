from www import app
from flask import make_response, jsonify, request

doctors = [
    {
    "user_id": 1,
    "username": "espanta",
    "email": "espanta@gmail.com",
    "name": "Espanta",
    "surname": "Murissoca",
    "age": 21,
    "specialty": ["Mopologista", "Melcacologista"],
    "gender": "male",
    "appointments": [{
        "appointment_id": 77,
        "patient": {
            "name": "Andre Saraiva",
            "age": 21
        },
        "schedule": {
            "from": "2011-07-14T22:01:00.947Z",
            "to": "2011-07-14T22:01:15.4354Z",
        },
        "clinic": {
            "clinic_id": 23,
            "name": "Clinica bizurada",
            "address": {
                "street": "Rua H8-B",
                "number": "212",
                "complement": "Vaga B",
                "neighborhood": "CTA",
                "city": "Sao Jose dos Campos",
                "state": "Sao Paulo",
                "country": "Brasil"
                }
            }

        }]
    }
]

patients = [{
    "user_id": 2,
    "username": "andresnds",
    "email": "andresnds@hotmail.com",
    "name": "Andre",
    "surname": "Saraiva",
    "age": 21,
    "gender": "male",
    "appointments": [
        {
            "appointment_id": 77,
            "doctor": {
                "name": "Espanta Murissoca",
                "specialty": ["Mopologista", "Melcacologista"],
            },
            "schedule": {
                "from": "2011-07-14T22:01:00.947Z",
                "to": "2011-07-14T22:01:15.4354Z",
            },
            "clinic": {
                "clinic_id": 23,
                "name": "Clinica bizurada",
                "address": {
                    "street": "Rua H8-B",
                    "number": "212",
                    "complement": "Vaga B",
                    "neighborhood": "CTA",
                    "city": "Sao Jose dos Campos",
                    "state": "Sao Paulo",
                    "country": "Brasil"
                }
            }
        }
    ],
}]

#TODO trocar tudo por services que se comunicam com DB


@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify( {'doctors': doctors} )


@app.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = filter(lambda p: p['user_id']==doctor_id, doctors)
    if len(doctor)>0:
        return jsonify(doctor[0])
    abort(404)


@app.route('/doctors', methods=['PUT'])
def insert_doctor():
    if not request.json:
        abort(400)
    doctor = request.json()
    doctor['user_id'] = doctors[-1]['user_id']+1
    doctors.append(doctor)
    return doctor


@app.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = filter(lambda p : p['user_id']==patient_id, patients)
    if len(patient)>0:
        return jsonify(patient[0])
    abort(404)

@app.route('/patients', methods=['PUT'])
def insert_patient():
    if not request.json:
        abort(400)
    patient = request.json()
    patient['user_id'] = patients[-1]['user_id']+1
    patients.append(patient)
    return patient

