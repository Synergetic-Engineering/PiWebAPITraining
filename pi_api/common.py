import requests
import datetime
import pytz
from config import pi_system
from config.pi_system import PI_WEB_API_BASE_URL, PI_AUTH, PI_AUTH_METHOD
import logging
log = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings() # PISRV and PICORESRV use self signed certificates


def unixtime_to_pi_timestamp(unix_time):
    dt = datetime.datetime.utcfromtimestamp(unix_time)
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def datetime_to_pi_timestamp(dt):
    dt_utc = dt.astimezone(pytz.UTC)
    return dt_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

def as_safe_path(resource_path):
    # Make the resource_path safe to post as JSON/UEL
    # i.e replace spaces with %20
    return resource_path#.replace(' ', '%20')

def connect_pi_web_api():
    # Test connection to Pi Web api with a GET request to the base URL
    r = requests.get(PI_WEB_API_BASE_URL, auth=PI_AUTH, verify=False)
    if r.status_code == 200:
        log.info('Connection to %s OK.' %PI_WEB_API_BASE_URL)
        return True
    else:
        log.error("Error connecting to %s - %s, %s" %(PI_WEB_API_BASE_URL, r.status_code, r.text))
        log.error("Make sure the Authentication method of the PiWebApi server matches '%s'" %PI_AUTH_METHOD)
        return False

def web_api_call(method='GET', endpoint="", params=None, json_payload=None):
   
    url = "%s/%s" %(PI_WEB_API_BASE_URL, endpoint)
    log.debug('API URL: %s' %url)
    log.debug('API params: %s' %params)
    log.debug('API PL: %s' %json_payload)
    header = {'Content-Type': 'application/json'}
    if method == "GET":
        return requests.get(url, params=params, auth=PI_AUTH, verify=False)
    if method == "POST":
        return requests.post(url, params=params, auth=PI_AUTH, headers=header, verify=False, json=json_payload)
    if method == "PATCH":
        return requests.patch(url, params=params, auth=PI_AUTH, headers=header,verify=False, json=json_payload)
    if method == "PUT":
        return requests.put(url, params=params, auth=PI_AUTH, headers=header,verify=False, json=json_payload)

def init_new_batch_request():
    return {}
    
def create_batch_step(method, resource, content={}, parameters=[], headers={}, parent_ids=[]):
    assert method in ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
    step_request = {
        "Method": method,
        "Resource": resource,
    }
    if content != {}:
        step_request["Content"] = content
    if parameters != []:
        step_request["Parameters"] = parameters
    if headers != {}:
        step_request["Headers"] = headers
    if parent_ids != {}:
        step_request["ParentIds"] = parent_ids
    return step_request

def add_to_batch_request(batch_list, next_step):
    if batch_list == {}:
        return 1, {1: next_step}
    else:
         last_index = int(sorted(batch_list.keys())[-1])
         index = last_index+1
         batch_list[index] = next_step
         return index, batch_list

def process_batch_request(batch_list):
    endpoint ="batch"
    json_pl = batch_list
    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 207:
        step_results = resp.json()
        for step_number in sorted(step_results.keys()):
            status_code = step_results[step_number]['Status']
            status_text = step_results[step_number]['Content']
            if status_code not in [200, 201, 204]:
                log.error("Error with batch request item: %s - %s: %s" %(step_number, status_code, status_text))
        return step_results
    else:
        log.error("Error submitting BATCH request!")
        log.error("%s: %s" %(resp.status_code, resp.text))
        return False
