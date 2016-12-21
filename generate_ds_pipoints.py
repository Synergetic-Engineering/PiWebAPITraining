from pi_api import data_archive
from config import kogancreek_model as site_model
from config.pi_system import AF_SERVER_PATH, DS_SERVER_PATH

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Get the Webid of the data server
ds_webid = data_archive.get_ds_server_webid(ds_server_path=DS_SERVER_PATH)

for unit in site_model.site_unit_prefix.keys():
    unit_pf = site_model.site_unit_prefix[unit]
    for component_model in site_model.site_components:
        component_instances = site_model.site_components[component_model]
        for inst in component_instances:
            M = component_model(instance_name=inst)
            tags = M.generate_tag_info()
            log.info('Generating %s PiPoints for unit: %s: %s instance of %s' %(len(tags), unit_pf, inst, M.model_name))
            for tag in tags:
                units, descr = tags[tag]
                pi_point_name = '%s_%s_%s' %(site_model.site_tag_prefix, unit_pf, tag)
                pt_create_result = data_archive.create_pi_point(ds_server_webid=ds_webid, point_name=pi_point_name, point_descr=descr,
                 point_class='classic', point_data_type='Float32', point_eng_units=units)
                if pt_create_result is not None:
                    if pt_create_result == 0:
                        log.info('Pi Point %s created successfully.' %pi_point_name)
                    elif pt_create_result == 1:
                        log.info('Pi Point %s already exists - updating configuration.' %pi_point_name)
                        pt_web_id = data_archive.get_pi_point_webid_by_path(pi_point_path="%s\\%s" %(DS_SERVER_PATH,pi_point_name))
                        data_archive.reconfigure_pi_point(pi_point_webid=pt_web_id, point_name=pi_point_name, point_descr=descr, point_eng_units=units)
                    else:
                        pass
                    