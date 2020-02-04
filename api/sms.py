from kavenegar import KavenegarAPI, APIException, HTTPException

api = KavenegarAPI('')


def verify(phone, password):
    try:
        params = {
            'receptor': str(phone),
            'token': password,
            'template': 'verify'
        }
        response = api.verify_lookup(params)
        return response
    except APIException as e:
        return e
    except HTTPException as e:
        return e


def send_sms(phone, message):
    try:
        params = {
            'receptor': str(phone),
            'message': message,
        }
        response = api.sms_send(params)
        return response
    except APIException as e:
        return e
    except HTTPException as e:
        return e
