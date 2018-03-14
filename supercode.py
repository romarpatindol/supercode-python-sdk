import urllib2
import json

HOSTED_FUNCTIONS_BASE_URL = "https://super-code.appspot.com/api/v1/function/{}"

STATUS_SUCCESS = 200


# Custom errors ------------------------------------------------------------
class Error(Exception):
    status = 500
    code = "ERROR"

    def __str__(self):
        return str(self.message)


class UnauthorizedRequest(Error):
    default_message = "No valid authentication details were provided. Access is denied."

    def __init__(self, message=default_message):
        self.code = "UNAUTHORIZED_REQUEST"
        self.message = message or self.default_message


class FunctionError(Error):
    default_message = "An unknown error occurred."

    def __init__(self, message=default_message):
        self.code = "UNKNOWN_ERROR"
        self.message = message or self.default_message


class FunctionNotFound(Error):
    default_message = "Function does not exist."

    def __init__(self, message=default_message):
        self.code = "FUNCTION_NOT_FOUND"
        self.message = message or self.default_message


class ServerError(Error):
    default_message = "Something occurred unexpectedly in the server. Please try again."

    def __init__(self, message=default_message):
        self.code = "SERVER_ERROR"
        self.message = message or self.default_message


# Callable functions -------------------------------------------------------
def call(function_name, _api_key, **kwargs):
    """Calls a function uploaded in Symph Hosted Functions

    :param function_name: The unique name of an existing function
    :param kwargs: Parameters to pass
    :return: Response in JSON format
    """
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = _api_key

    # dump arguments to JSON string
    arguments = json.dumps(kwargs)

    # build urllib2.Request object
    request = urllib2.Request(
        url=HOSTED_FUNCTIONS_BASE_URL.format(function_name),
        data=arguments,
        headers=headers
    )

    # send HTTP request
    data = None
    try:
        response = urllib2.urlopen(request, timeout=60)
        if response.getcode() == STATUS_SUCCESS:
            data = response.read()
    except urllib2.HTTPError, exc:
        try:
            response = json.loads(exc.read())
            status_code = response.get("code")
            if status_code == 401:
                raise UnauthorizedRequest(response.get("message"))
            elif status_code == 404:
                raise FunctionNotFound(response.get("message"))
            else:
                raise FunctionError(response.get("message"))
        except ValueError:
            raise ServerError()

    # try to JSON Parse
    try:
        data = json.loads(data)
    except ValueError:
        pass

    return data
