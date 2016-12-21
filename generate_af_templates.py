from pi_api import asset_server
from pi_api.common import as_safe_path
from config import kogancreek_model as site_model
from config.pi_system import AF_DB_NAME, AF_SERVER_PATH, DS_SERVER_PATH

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Get the Webid of the asset server
af_webid = asset_server.get_af_server_webid(af_server_path=AF_SERVER_PATH)

# Create a new database in the Asset server
asset_server.create_af_database(database_name=AF_DB_NAME, af_server_webid=af_webid, database_descr='AF database for PiWebApi training final project')
# Get the Webid of the asset server database
db_webid = asset_server.get_af_database_webid(af_server_path=AF_SERVER_PATH, database_name=AF_DB_NAME)
af_db_path = as_safe_path('%s\\%s' %(AF_SERVER_PATH, AF_DB_NAME))


# Create Element and Attribute templates for component types in the site model 
for component_model in site_model.site_components:
    # Create an instance of the component model
    i = component_model(instance_name='config')
    # Createa an element template for the component model
    log.info('Creating AF Element Template for component type: %s' %i.model_name)
    asset_server.create_element_template(element_template_name=i.model_name, db_web_id=db_webid, element_template_descr='Template for %s Sentient Model' %i.model_name)
    et_webid = asset_server.get_element_template_webid(element_template_name=i.model_name, db_web_id=db_webid)
    af_et_path = as_safe_path('%s\\ElementTemplates[%s]' %(af_db_path, i.model_name))

    # Add attributes for site_tag_prefix
    attrib_config = {
            'Name': 'site_tag_prefix',
            "Description": 'Site prefix for Sentient model instance',
            "Type": "String",
            "DataReferencePlugIn": '',
            "ConfigString": '',
        }
    result = asset_server.create_attribute_template(template_config=attrib_config, element_template_web_id=et_webid)
    if result == 1:
        # Attribute template already exists so just update the config
        af_at_path = as_safe_path('%s|%s' %(af_et_path, 'site_tag_prefix'))
        attr_webid = asset_server.get_attribute_template_webid(attribute_template_path=af_at_path)
        asset_server.update_attribute_template(atrib_template_web_id=attr_webid, update_config=attrib_config)


    # Add attributes for site_unit_prefix
    attrib_config = {
            'Name': 'site_unit_prefix',
            "Description": 'Unit prefix for Sentient model instance',
            "Type": "String",
            "DataReferencePlugIn": '',
            "ConfigString": '',
        }
    result = asset_server.create_attribute_template(template_config=attrib_config, element_template_web_id=et_webid)
    if result == 1:
        # Attribute template already exists so just update the config
        af_at_path = as_safe_path('%s|%s' %(af_et_path, 'site_unit_prefix'))
        attr_webid = asset_server.get_attribute_template_webid(attribute_template_path=af_at_path)
        asset_server.update_attribute_template(atrib_template_web_id=attr_webid, update_config=attrib_config)
    
    # Add attributes for each measure on the model
    for meas in sorted(i.measures):
        log.info('Adding AF Attribute Template for measure: %s to component: %s' %(i.model_name, meas))
        units, desc = i.measures[meas]
        attrib_config = {
            'Name': meas,
            "Description": desc,
            "Type": "Double",
            "DefaultUnitsName": units,
            "DataReferencePlugIn": 'PI Point',
            "ConfigString": '%s\\%%@site_tag_prefix%%_%%@site_unit_prefix%%_%%Element%%.%s'  %(DS_SERVER_PATH, meas)
        }
        result = asset_server.create_attribute_template(template_config=attrib_config, element_template_web_id=et_webid)
        if result == 1:
            # Attribute template already exists so just update the config
            af_at_path = as_safe_path('%s|%s' %(af_et_path, meas))
            attr_webid = asset_server.get_attribute_template_webid(attribute_template_path=af_at_path)
            asset_server.update_attribute_template(atrib_template_web_id=attr_webid, update_config=attrib_config)

