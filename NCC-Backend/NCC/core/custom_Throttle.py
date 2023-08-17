from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled): # check that a Throttled exception is raised
        custom_response_data = { # prepare custom response data
            'msg': 'Too many requests. Please wait and try again later.',
            'availableIn': '%d seconds'%exc.wait
        }
        response.data = custom_response_data # set the custom response data on response object

    return response