import sys
import csv
from pi_api import data_archive
from pi_api.common import unixtime_to_pi_timestamp
from config.pi_system import DS_SERVER_PATH

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Get the Webid of the data server
ds_webid = data_archive.get_ds_server_webid(ds_server_path=DS_SERVER_PATH)

# Get the name of the data csv file from the command line argument
csv_file_name = sys.argv[1]


with open(csv_file_name) as fp:
    csv_data = csv.DictReader(fp)
    # Get tag names from the header row of the CSV file, exclude the 'UnixTime' field
    tag_names = ['%s' %fn for fn in csv_data.fieldnames if fn != 'UnixTime']
    # Check tag names in CSV file correspond to PiPoints
    # Create the Pi Pount path using the data archive server path 
    point_paths = ['%s\\%s' %(DS_SERVER_PATH, t) for t in tag_names]
    # Create a tag name to PiPoint WebId lookup dict
    tag_webid_lookup = data_archive.get_webids_for_pipoints(point_path_list=point_paths)

    log.info('%s tags found in: %s' %(len(tag_names), csv_file_name))

    data_for_points = {}
    row_count = 0
    # Iterate through each row of the CSV file
    for row in csv_data:
        # Create a value time stamp from the UnixTime field of the row
        timestamp = unixtime_to_pi_timestamp(unix_time=float(row['UnixTime']))
        row_count +=1
        # Iterate through each column of the row, putting the value for each tag into a list of timestamped values
        # grouped by the WebId of the tag/Pi point
        for tag in tag_names:
            tag_webid = tag_webid_lookup.get(tag)
            if tag_webid is not None:
                if tag_webid not in data_for_points:
                    data_for_points[tag_webid] = []
                try:
                    # Check that the value for the tag is actually numeric, otherwise do not add it to the timestamped values list    
                    val = float(row[tag])
                    data_for_points[tag_webid].append({'Timestamp': timestamp,'Value': val})
                except ValueError:
                    log.warn('Invalid float value: "%s" for tag: %s, @ %s. This value will NOT be written to Pi.' %(row[tag], tag, timestamp))
            else:
                log.warn('Could not find WebID for tag %s' %tag)
    log.info('%s time entries found in %s' %(row_count, csv_file_name))

# Write the data sets to Pi grouped by the point WebId
for webid in data_for_points.keys():
    if data_archive.write_values_for_pi_point(pi_point_webid=webid, timestamped_values=data_for_points[webid], update_option='Replace'):
        log.info('%s values successfully written to Pi Point: %s' %(len(data_for_points[webid]), webid))
    else:
        log.error('Error encounted while writing data set to PI. See above error for details.')
