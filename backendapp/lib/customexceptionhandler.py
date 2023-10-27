from rest_framework.views import exception_handler
from backendapp.lib.custom_response import CustomResponse
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_501_NOT_IMPLEMENTED, HTTP_400_BAD_REQUEST

def custom_exception_handler(exc, context):
	"""
	Custom exception handler for Django Rest Framework that adds
	the `status_code` to the response and renames the `detail` key to `error`.
	"""
	response = exception_handler(exc, context)
	import traceback
	stack = traceback.format_exc()
	# logger.exception(stack)

	if response is not None:
		response =  CustomResponse(message=exc.detail, code=exc.status_code)

	else:
		message = None
		code = HTTP_501_NOT_IMPLEMENTED

		if exc.__class__.__name__ == 'DoesNotExist':
			code = HTTP_500_INTERNAL_SERVER_ERROR
			message = exc.message

		elif (exc.__class__.__name__ == 'KeyError') or (exc.__class__.__name__ == 'MultiValueDictKeyError'):
			code = HTTP_400_BAD_REQUEST
			try:
				message = 'Bad request must pass %s' % exc.message
			except Exception as e:
				message = 'Missing key in request data, please check'

		elif exc.__class__.__name__ == 'ValidationError':
			code = HTTP_400_BAD_REQUEST
			message = exc.message

		elif exc.__class__.__name__ == 'IntegrityError':
			code = HTTP_400_BAD_REQUEST
			message = exc[1]

		elif exc.__class__.__name__ == 'error':
			code = HTTP_500_INTERNAL_SERVER_ERROR
			message = 'socket error'

		else:
			code = HTTP_500_INTERNAL_SERVER_ERROR
			message = "Unhandled Exception"

		response =  CustomResponse(message=message, code=code)
	return response