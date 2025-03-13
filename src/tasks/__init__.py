from core.celery import app
from models import Patient
from loguru import logger
import random

from repositories.patient import PatientRepository
@app.task(bind=True, max_retries=3)
def send_notification(self, patient_id: 'int'):

    try:
        patient_repository = PatientRepository(sync=True)
        patient = patient_repository.find_one(id=patient_id)
        if random.random() < 0.25:
            raise Exception('Simulated task failure')
        
        print(f'Notification sent successfully to [{patient.name}].')

        logger.info(f'Notification sent successfully to [{patient.name}].')

    except Exception as e:
        print(f"Error occured: {e}")
        raise self.retry(exc=e, countdown=5)
