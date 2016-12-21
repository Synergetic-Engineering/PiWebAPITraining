from pi_api.common import web_api_call
from pi_api.common import unixtime_to_pi_timestamp
from pi_api.common import init_new_batch_request, create_batch_step, add_to_batch_request, process_batch_request
from config.pi_system import PI_WEB_API_BASE_URL

import logging
log = logging.getLogger(__name__)


def get_ds_server_webid(ds_server_path):
    endpoint = "dataservers"
    parameters = {
        'path': ds_server_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for DS server %s" %ds_server_path)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None        

def create_pi_point(ds_server_webid, point_name, point_descr='', point_class='classic', point_data_type='Float32', point_eng_units='', point_dig_set_name='True'):
    endpoint = "dataservers/%s/points" %ds_server_webid
    json_pl = {
        "Name": point_name,
        "Descriptor": point_descr,
        "PointClass": point_class,
        "PointType": point_data_type,
        "EngineeringUnits": point_eng_units,
    }
    if point_data_type == "Digital":
        json_pl['DigitalSetName'] = point_dig_set_name

    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 201:
        return 0
    elif resp.status_code == 400:
        log.warn("PI Point: %s already exists" %point_name)
        return 1
    else:
        log.error("Error creating PI Point %s" %point_name)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def get_pi_point_webid_by_path(pi_point_path):
    endpoint = "points"
    parameters = {
        'path': pi_point_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for PI Point %s" %pi_point_path)
        log.error("%s: %s" %(resp.status_code, resp.text))   
        return None

def reconfigure_pi_point(pi_point_webid, point_name, point_descr=None, point_eng_units=None):
    endpoint = "points/%s" %pi_point_webid
    json_pl = {
        "Name": point_name,
    }
    if point_descr is not None:
        json_pl["Descriptor"] = point_descr
    if point_eng_units is not None:
        json_pl["EngineeringUnits"] = point_eng_units

    resp = web_api_call(method='PATCH', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 204:
        return True
    else:
        log.error("Error re-configuring PI Point %s" %point_name)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return False

def get_webids_for_pipoints(point_path_list):
    # create a batch request to get webids for a list of point names
    endpoint='points'
    base_resource = '%s/%s' %(PI_WEB_API_BASE_URL, endpoint)
    BR = init_new_batch_request()
    for point_name in point_path_list:
        param_str = 'path=%s&selectedFields=WebId;Name' %point_name
        resource = '%s?%s' %(base_resource,param_str)
        step = create_batch_step(method='GET',resource=resource,parameters=[])
        i, BR = add_to_batch_request(batch_list=BR,next_step=step)

    results = process_batch_request(batch_list=BR)
    point_webids = {}
    for r in results:
        if results[r]['Status'] == 200:
            point_webid = str(results[r]['Content']['WebId'])
            point_name = str(results[r]['Content']['Name'])
            point_webids[point_name] = point_webid
    return point_webids
            
def write_values_for_pi_point(pi_point_webid, timestamped_values, update_option='Replace'):
    # Write timestamped values to the pi point using the streams endpoint
    endpoint = "streams/%s/recorded" %pi_point_webid
    parameters = {
        'updateOption': update_option,
     }
    json_pl = []
    for tsv in timestamped_values:
        json_pl.append(tsv)

    resp = web_api_call(method='POST', endpoint=endpoint, params=parameters, json_payload=json_pl)
    if resp.status_code in [202, 204]: # 202 status code indicates that the request has been accepted but not yet completed
        return True
    else:
        log.error("Error writing values to PI Point!")
        log.error("%s: %s" %(resp.status_code, resp.text))
        return False

