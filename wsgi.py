from router import Router
from utils import parse_http_x_www_form_urlencoded_post_data, \
    parse_http_get_data, parse_http_headers, \
    parse_http_content_type, parse_http_uri


DEBUG = False
STATIC_URL = '/resources/'
STATIC_ROOT = 'data'

# Instantiate the router
router = Router()
# List all routes here
router.get('/', 'ConvolutionCorrelationController@index')
router.get('/sharpen', 'SharpeningController@sharpen')
router.get('/filter', 'FilteringController@filtering')
router.get('/smoothing', 'SmoothingController@smoothing')


def application(environ, start_response):
    # https://www.python.org/dev/peps/pep-3333/#environ-variables
    REQUEST_METHOD = environ['REQUEST_METHOD']
    CONTENT_TYPE, CONTENT_TYPE_KWARGS = parse_http_content_type(environ)
    SERVER_PROTOCOL = environ['SERVER_PROTOCOL']
    HEADERS = parse_http_headers(environ)
    URI_PATH = environ['PATH_INFO'].strip('/')
    URI = parse_http_uri(environ)
    POST = parse_http_x_www_form_urlencoded_post_data(environ)
    GET = parse_http_get_data(environ)

    headers = [('Content-type', 'text/html; charset=utf-8')]
    headers.extend([('Access-Control-Allow-Origin', '*')])
    params = {
        "request_method": REQUEST_METHOD,
        "uri_path": URI_PATH,
        "get": GET,
        "post": POST,
        "headers": headers,
    }
    if len(GET) > 0:
        query_string = environ['QUERY_STRING']
        get_params = query_string.split('&')
        for var in get_params:
            key, value = var.split('=')
            params[key] = value

    controller_callback = router.resolve(REQUEST_METHOD, URI_PATH)
    status, body = controller_callback(params, params)
    if URI_PATH.startswith(STATIC_URL):
        print('STATIC FILE DETECTED!')

    if DEBUG:
        print("{REQUEST_METHOD} {URI_PATH} {SERVER_PROTOCOL}\n"
              "CONTENT_TYPE: {CONTENT_TYPE}; {CONTENT_TYPE_KWARGS}\n"
              "POST: {POST}\n"
              "GET: {GET}\n"
              ":HEADERS:\n{HEADERS}\n"
              .format(**locals()))

    start_response(status, headers)
    return [body]
