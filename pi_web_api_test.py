import sys
from pi_api import common
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('Testing connection to PI Web API...')
if not common.connect_pi_web_api():
    sys.exit(1)
else:
     log.info('Connection to PI WebAPI service successfull.')
     sys.exit(0)