from kavenegar import *
from django.conf import settings
from celery import shared_task


# send OTP sms (needs template)
@shared_task
def send_otp_sms(phone_number: str, code: str):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': settings.KAVENEGAR_OTP_TEMPLATENAME,
            'token': code,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params=params)
        settings.LOGGER.info(f"OTP sms sent successfully to {response[0]['receptor']}")
        return 'OTP successfully'
    except (APIException, HTTPException) as e:
        exception_name = type(e).__name__
        exception_message = str(e)
        settings.LOGGER.error(f"{exception_name} sending OTP to {phone_number}: {exception_message}")
        return {'status': 'error', 'error': exception_name, 'message': exception_message}


@shared_task
def send_verify_order_sms(phone_number, order_id):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_APIKEY)
        params = {
            'receptor': phone_number,
            'template': settings.KAVENEGAR_VERIFYORDER_TEMPLATENAME,
            'token': order_id,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params=params)
        return {'status': True, 'message': f'Verify order sms sent successfully to {response[0]["receptor"]}'}
    except (APIException, HTTPException) as e:
        exception_name = type(e).__name__
        exception_message = e.args[0].decode()
        settings.LOGGER.error(f"{exception_name} Verify order sms {phone_number}: {exception_message}")
        return {'status': False, 'message': f'Verify order sms {exception_name} error : {exception_message}'}
