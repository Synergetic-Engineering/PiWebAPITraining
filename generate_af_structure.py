from pi_api import asset_server
from pi_api.common import as_safe_path
from config import kogancreek_model as site_model
from config.pi_system import AF_DB_NAME, AF_SERVER_PATH, DS_SERVER_PATH

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Get the Webid of the asset server
af_webid = asset_server.get_af_server_webid(af_server_path=AF_SERVER_PATH)

# Get the Webid of the asset server database
db_webid = asset_server.get_af_database_webid(af_server_path=AF_SERVER_PATH, database_name=AF_DB_NAME)
af_db_path = as_safe_path('%s\\%s' %(AF_SERVER_PATH, AF_DB_NAME))


# Generate top level AF elements - (simple elements)

# Corp location
log.info('Creating Corpoate level AF Element: %s' %site_model.corp_name)
asset_server.create_af_element(element_name=site_model.corp_name, parent_web_id=db_webid, is_root_element=True)
af_corp_path = as_safe_path('%s\\%s' %(af_db_path, site_model.corp_name))
corp_webid = asset_server.get_af_element_webid(af_element_path=af_corp_path)

# Site Location
log.info('Creating Site Location AF Element: %s' %site_model.site_name)
asset_server.create_af_element(element_name=site_model.site_name, parent_web_id=corp_webid)
af_site_path = as_safe_path('%s\\%s' %(af_corp_path, site_model.site_name))
site_webid = asset_server.get_af_element_webid(af_element_path=af_site_path)


# Site Unit(s)
for unit_name in site_model.site_units:
    log.info('Creating Site Unit AF Element: %s' %unit_name)
    asset_server.create_af_element(element_name=unit_name, parent_web_id=site_webid)
    af_unit_path = as_safe_path('%s\\%s' %(af_site_path, unit_name))
    unit_webid = asset_server.get_af_element_webid(af_element_path=af_unit_path)

    # Logical plant blocks
    for lb in site_model.site_blocks:
        log.info('Creating Unit %s logical block AF Element: %s' %(unit_name, lb))
        asset_server.create_af_element(element_name=lb, parent_web_id=unit_webid)
        af_lb_path = as_safe_path('%s\\%s' %(af_unit_path, lb))
        lb_webid = asset_server.get_af_element_webid(af_element_path=af_lb_path)
       

    # Generate AF elements using templates
    for component_model in site_model.site_components:
        component_instances = site_model.site_components[component_model]
        for inst in component_instances:
            M = component_model(instance_name=inst)
            lb_name = M.get_block_name()
            # Get the parent logical block
            af_lb_path = as_safe_path('%s\\%s' %(af_unit_path, lb_name))
            lb_webid = asset_server.get_af_element_webid(af_element_path=af_lb_path)
            log.info('Creating %s AF element %s from %s template' %(unit_name, inst, M.model_name))
            asset_server.create_af_element(element_name=M.name, parent_web_id=lb_webid, element_descr='', is_root_element=False, template_name=M.model_name)
            # Set the 'site_tag_prefix' and 'site_unit_prefix' attribues on the element
            tag_prefix_attr_webid = asset_server.get_af_attrib_webid(af_attrib_path='%s\\%s|%s' %(af_lb_path,M.name,'site_tag_prefix'))
            unit_prefix_attr_webid = asset_server.get_af_attrib_webid(af_attrib_path='%s\\%s|%s' %(af_lb_path,M.name,'site_unit_prefix'))
            asset_server.update_attribute_value(af_attrib_web_id=tag_prefix_attr_webid, new_value=site_model.site_tag_prefix)
            asset_server.update_attribute_value(af_attrib_web_id=unit_prefix_attr_webid, new_value=site_model.site_unit_prefix[unit_name])

           
