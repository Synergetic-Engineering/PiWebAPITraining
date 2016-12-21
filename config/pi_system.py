from requests.auth import HTTPBasicAuth
from requests_kerberos import HTTPKerberosAuth, REQUIRED

PI_WEB_API_BASE_URL = 'https://pisrv/piwebapi' # URL of the Pi Web API service

AF_SERVER_PATH = '\\\\PISRV' # AF server path as seen by the Pi web API
DS_SERVER_PATH = '\\\\PISRV' # Data archive server path as seen by the Pi web API
AF_DB_NAME = 'PiWebApiTrainingFinal' # The AF database to work with - can be already existing

# Pi Web API HTTP authentication settings
PI_USR = None # user name for basic auth
PI_PWD = None # password for basic auth
PI_AUTH_METHOD = 'Basic' # Basic or Kerberos methods can be used
KERBEROS_AUTH_STR = None    # use a specific account for Kerberos auth in the format: user@realm:password, otherwise set to None
                                                # to use currently logged on user

if PI_AUTH_METHOD == 'Basic':
    # Basic authentication
    if not PI_USR is None and not PI_PWD is None:
        PI_AUTH = HTTPBasicAuth(PI_USR, PI_PWD)
    else:
        print 'PI System credentials not set!'
        print 'Set the PI_USR and PI_PWD variables in config/pi_system.py before proceeding.'
elif PI_AUTH_METHOD =='Kerberos':
    # Kerbros authentication
    if KERBEROS_AUTH_STR is not None:
        # use a specified account
        PI_AUTH = HTTPKerberosAuth(principal=KERBEROS_AUTH_STR)
    else:
        # use account of the user running this script/app
        PI_AUTH = HTTPKerberosAuth()
else:
    print 'Authentication method not set!'
    print 'Set the PI_AUTH_METHOD variable in config/pi_system.py to "Basic" or "Kerberos" before proceeding.'
    


