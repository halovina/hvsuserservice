from datetime import datetime
import json
import time, socket, logging
from datetime import datetime
from wsgiref.util import request_uri

request_log = logging.getLogger("api")

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        now = datetime.now()
        log_data = {
            "remote_address": request.META['REMOTE_ADDR'],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }
        response = ""
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
            if request.get_full_path() == '/api/v1/users/login':
                log_data['password'] = 'xxxxxx'
            log_data['request_body'] = req_body
            response = self.get_response(request)
            if response and response["content-type"] == "application/json":
                response_body = json.loads(response.content.decode("utf-8"))
                log_data['response_body'] = response_body
            else:
                log_data['response_body'] = {}
            log_data['run_time'] = time.time() - start_time
            log_data['xtime'] = now.strftime("%Y-%m-%d %H:%M:%S")
            request_log.info(log_data)
        return response
    
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_log.exception("Unhandle Exception {}".format(str(e)))
        return exception