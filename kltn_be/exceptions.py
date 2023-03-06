from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail
from http import HTTPStatus
from raven.contrib.django.raven_compat.models import client


def api_exception_handler(exc, context):
    client.captureException()
    response = exception_handler(exc, context)
    http_code_to_message = {v.value: v.description for v in HTTPStatus}
    status_code = 500
    error_payload = {
        'error': {'detail': 'Server error'},
        'message': http_code_to_message[status_code],
        'code': status_code,
        'is_error': True
    }
    if response is not None:
        if isinstance(response.data, dict):
            if 'warning' in response.data.keys():
                error_payload['warning'] = response.data['warning']
                error_payload['is_error'] = False
            else:
                custom_response = {}
                for key, value in response.data.items():
                    if value and isinstance(value, list) and isinstance(value[0], ErrorDetail):
                        custom_response[key] = str(value[0])
                    if isinstance(value, ErrorDetail):
                        custom_response[key] = str(value)
                response.data = custom_response
                error_payload['error'] = response.data
        else:
            error_payload['error'] = response.data
        status_code = response.status_code
        error_payload['message'] = http_code_to_message[status_code]
        error_payload['code'] = status_code
    return Response(error_payload, status=status.HTTP_200_OK)
