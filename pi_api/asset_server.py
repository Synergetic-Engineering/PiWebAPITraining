from pi_api.common import unixtime_to_pi_timestamp
from pi_api.common import web_api_call

import logging
log = logging.getLogger(__name__)


def get_af_server_webid(af_server_path):
    # Get the webID of an asset server given its path
    endpoint = "assetservers"
    parameters = {
        'path': af_server_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for AF server %s" %af_server_path)
        log.error("%s: %s" %(resp.status_code, resp.text))

def create_af_database(database_name, af_server_webid, database_descr=''):
    # Create a new DB on the asset server
    # Return 0 if a new DB is created, 1 if a DB by the same name already exists
    endpoint = "assetservers/%s/assetdatabases" %af_server_webid
    json_pl = {
        "Name": database_name,
        "Description": database_descr,
    }
    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 201:
        return 0
    elif resp.status_code == 409:
        log.warn("Asset database: %s already exists" %database_name)
        return 1
    else:
        log.error("Error creating Asset Database %s" %database_name)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def get_af_database_webid(af_server_path, database_name):
    # Return WebID of an AF DB
    endpoint = "assetdatabases"
    parameters = {
        'path': '%s\\%s' %(af_server_path, database_name),
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for Asset Database %s on AF server: %s" %(database_name, af_server_path))
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def create_element_template(element_template_name, db_web_id, element_template_descr=''):
    # Create a new element template
    # Return 0 if a new template is created or 1 if a template by the same name already exists
    endpoint = "assetdatabases/%s/elementtemplates" %db_web_id
    json_pl = {
        "Name": element_template_name,
        "Description": element_template_descr,
        "InstanceType": "Element",
        }
    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 201:
        return 0
    elif resp.status_code == 409:
        log.warn("Element template: %s already exists" %element_template_name)
        return 1
    else:
        log.error("Error creating Element template %s" %element_template_name)
        log.error('%s: %s' %(resp.status_code, resp.text))
        return None

def get_element_template_webid(element_template_name, db_web_id):
    # Return WebID of an Element template
    endpoint = "assetdatabases/%s/elementtemplates" %db_web_id
    parameters = {
        'field': 'Name',
        'query': '%s' %element_template_name,
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['Items'][0]['WebId']
    else:
        log.error("Error retrieving WebID for Element template %s" %element_template_name)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def create_attribute_template(template_config, element_template_web_id):
    # Create a new attribute template using the supplied template_config
    # Return 0 if a new template is created or 1 if a template by the same name already exists
    endpoint = "elementtemplates/%s/attributetemplates" %element_template_web_id
    json_pl = template_config
    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 201:
        return 0
    elif resp.status_code == 409:
        log.warn("Attribute template: %s already exists" %template_config['Name'])
        return 1
    else:
        log.error("Error creating Attribute template %s" %template_config['Name'])
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def get_attribute_template_webid(attribute_template_path):
    # Return WebID of an Attribute template
    endpoint = "attributetemplates"
    parameters = {
        'path': attribute_template_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for Attribute template %s" %attribute_template_path)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None    

def update_attribute_template(atrib_template_web_id, update_config):
    # Update an existing attribute template
    endpoint = "attributetemplates/%s" %atrib_template_web_id
    json_pl = update_config
    resp = web_api_call(method='PATCH', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 204:
        return True
    else:
        log.error("Error updating Attribute template %s" %update_config['Name'])
        log.error("%s: %s" %(resp.status_code, resp.text))
        return False

def create_af_element(element_name, parent_web_id, element_descr='', is_root_element=False, template_name=None):
    # Create an an AF element, using a template if template_name is supplied
    # A root element needs to be created using the assetdatbases endpoint
    # Return 0 if a new element is created or 1 if an element by the same name already exists
    if is_root_element:
        endpoint = "assetdatabases/%s/elements" %parent_web_id
    else:
        endpoint = "elements/%s/elements" %parent_web_id
    json_pl = {
        "Name": element_name,
        "Description": element_descr,
    }
    if template_name is not None:
        json_pl["TemplateName"] = template_name

    resp = web_api_call(method='POST', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 201:
        return 0
    elif resp.status_code == 409:
        log.warn("Element : %s already exists" %element_name)
        return 1
    else:
        log.error("Error creating Element %s" %element_name)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def get_af_element_webid(af_element_path):
    # Return WebID of AF element
    endpoint = "elements"
    parameters = {
        'path': af_element_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for AF element %s" %af_element_path)
        log.error("%s: %s" %(resp.status_code, resp.text))

def get_af_attrib_webid(af_attrib_path):
    # Return WebID of an AF attribute
    endpoint = "attributes"
    parameters = {
        'path': af_attrib_path,
        'selectedFields': 'WebId',
    }
    resp = web_api_call(method='GET', endpoint=endpoint, params=parameters, json_payload=None)    
    if resp.status_code == 200:
        return resp.json()['WebId']
    else:
        log.error("Error retrieving WebID for AF attribute: %s" %af_attrib_path)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return None

def update_attribute_value(af_attrib_web_id, new_value):
    # Update the value of an attribute
    endpoint = "attributes/%s/value" %af_attrib_web_id
    json_pl = {'Value': new_value}
    resp = web_api_call(method='PUT', endpoint=endpoint, params=None, json_payload=json_pl)
    if resp.status_code == 204:
        return True
    else:
        log.error("Error updating Attribute value %s" %new_value)
        log.error("%s: %s" %(resp.status_code, resp.text))
        return False