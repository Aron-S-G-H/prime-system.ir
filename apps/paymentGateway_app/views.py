from django.shortcuts import render
from utils.email import send_email_notif_to_admin
from utils.encrypt_data import is_valid_uuid
from apps.cart_app.models import UserOrder
from utils.sms import send_verify_order_sms
from django.core.cache import cache
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from PrimeSystem.settings import LOGGER

def verify(request, order_uuid):
    if order_uuid and is_valid_uuid(order_uuid):
        order_status = request.GET.get('status')
        order_id = cache.get(order_uuid)
        LOGGER.info(f'Verifying Order => \norderID: {order_id} \norderUUID: {order_uuid} \nstatus: {order_status}')
        if order_status == 'OK':
            send_email_notif_to_admin.apply_async(
                ('سفارش جدید', 'سفارش جدیدی در وبسایت ثبت شده است'),
                retry=False,
                ignore_result=True,
                expires=30,
            )
            try:
                user_order = UserOrder.objects.get(id=int(order_id))
                user_order.is_paid = True
                user_order.save()
                send_verify_sms = send_verify_order_sms.apply_async(
                    (user_order.phone, order_id+100),
                    retry=False,
                    ignore_result=False,
                    expires=30
                )
                sms_result = AsyncResult(send_verify_sms.task_id)
                try:
                    get_sms_result = sms_result.get(timeout=40)
                    LOGGER.warning(get_sms_result['message'])
                    if get_sms_result['status']:
                        user_order.is_sms_sent = True
                        user_order.save()
                except TimeoutError:
                    LOGGER.warning("Send Confirm SMS Task has not completed within the specified timeout")
                    sms_result.forget()
            except Exception as e:
                LOGGER.warning(f'Verifying Order Error - ORDER-ID:{order_id} - Status: {order_status} \n{e}')
            return render(request, 'paymentGateway_app/payment-ok.html')
        elif order_status == 'VOCE':
            LOGGER.warning(f'Verify Order Confirmation Error - Order ID: {order_id}')
            return render(request, 'paymentGateway_app/payment-nok.html', {'status': 'VOCE'})
        elif order_status == 'CT':
            LOGGER.warning(f'Verify Order Transaction Canceled, Order ID: {order_id}')
            return render(request, 'paymentGateway_app/payment-nok.html', {'status': 'CT'})
        elif order_status == 'TE':
            LOGGER.warning(f'Get Token error, Order ID: {order_id}')
            return render(request, 'paymentGateway_app/payment-nok.html', {'status': 'TE'})
        else:
            LOGGER.warning(f'Invalid or missing status order => status: {order_status}, order ID: {order_id}')
            return render(request, 'paymentGateway_app/payment-nok.html')
    LOGGER.warning('Missing or Invalid UUID => %s', order_uuid)
    return render(request, 'paymentGateway_app/payment-nok.html')
