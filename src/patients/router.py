from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from core.middleware.auth_middleware import token_required
from core.settings import get_application_settings
from core.validate import validate_email_and_password, validate_user
from repositories.patient import PatientRepository
from repositories.user import UserRepository
from models import User
import traceback
import jwt
from core.settings.app import app
import datetime
from loguru import logger

from tasks import send_notification

settings = get_application_settings()

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['POST'])
@token_required
def add_patient(current_user):
    try:
        body = request.json
        if not body:
            return {
                "message": "Invalid data, you need to give the patient name, email, phone number",
                "data": None,
                "error": "Bad request"
            }, 400
        
        patient_repository = PatientRepository(sync=True)

        new_patient = patient_repository.create(
            name=body.get('name'),
            email=body.get('email'),
            phone=body.get('phone')
        )
        
        if not new_patient:
            return {
                "message": "Patient already exists",
                "error": "Conflict",
                "data": None
            }, 409
        send_notification.delay(patient_id=new_patient.id)
        return {
            "message": "Successfully created new patient",
            "data": {
                'name': new_patient.name,
                'email': new_patient.email,
                'phone': new_patient.phone
            }
        }, 201
    except Exception as e:
        traceback.print_exc()
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@patient_bp.route('/patients', methods=['GET'])
@token_required
def get_patients(current_user):
    try:
        patient_repository = PatientRepository(sync=True)
        patients = patient_repository.find_all()
        serialized_patients = [patient.serialize() for patient in patients]
        return {
            "message": "Successfuly retrieved all patients",
            "data": serialized_patients
        }

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "message": "Failed to retrieve all patients",
            "data": None,
            "error": str(e)
        }), 500

@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
@token_required
def get_patient(current_user, patient_id):
    try:
        patient_repository = PatientRepository(sync=True)
        patient = patient_repository.find_one(id=patient_id)
        serialized_patient = patient.serialize()
        return {
            "message": "Successfuly retrieved a patient",
            "data": serialized_patient
        }

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "message": "Failed to retrieve all patients",
            "data": None,
            "error": str(e)
        }), 500

@patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@token_required
def update_patient(current_user, patient_id):
    try:
        patient = request.json
        patient_repository = PatientRepository(sync=True)
        patient0 = patient_repository.find_one(id=patient_id)
        patient0.name = patient.get('name')
        patient0.phone = patient.get('phone')
        patient0.email = patient.get('email')
        patient_repository.save(patient0)

        logger.info(f'[{current_user.name}] Updated patient information {patient0.name}')
        
        send_notification.delay(patient_id=patient0.id)

        return {
            "message": "Successfuly updated a patient",
            "data": {
                'name': patient0.name,
                'phone': patient0.phone,
                'email': patient0.email
            }
        }

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "message": "Failed to update a patient",
            "data": None,
            "error": str(e)
        }), 500


@patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
@token_required
def delete(current_user, patient_id):
    try:
        patient_repository = PatientRepository(sync=True)
        patient0 = patient_repository.find_one(id=patient_id)
        if patient0 is None:
            return jsonify({
                "message": "There is no such patient",
                "data": None,
            }), 400

        patient_repository.delete(patient0)

        logger.info(f'[{current_user.name}] removed patient information {patient0.name}')

        return {
            "message": "Successfuly removed a patient",
            "data": {
                'name': patient0.name,
                'phone': patient0.phone,
                'email': patient0.email
            }
        }

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "message": "Failed to update a patient",
            "data": None,
            "error": str(e)
        }), 500
