from pathlib import Path
BASE_PATH = Path().absolute()


STORIES_SERVICE_IP = '172.28.1.2'
STORIES_SERVICE_PORT = '5000'

USERS_SERVICE_IP = '172.28.1.3'
USERS_SERVICE_PORT = '5000'

DICE_SERVICE_IP = '172.28.1.4'
DICE_SERVICE_PORT = '5000'

PROFILING_SERVICE_IP = '172.28.1.5'
PROFILING_SERVICE_PORT = '5000'

REACTIONS_SERVICE_IP = '172.28.1.6'
REACTIONS_SERVICE_PORT = '5000'

LOGIN_URL = "http://{}:{}/login".format(USERS_SERVICE_IP, USERS_SERVICE_PORT)
SIGNUP_URL = "http://{}:{}/signup".format(USERS_SERVICE_IP, USERS_SERVICE_PORT)
GET_USER_URL = "http://{}:{}/user".format(USERS_SERVICE_IP, USERS_SERVICE_PORT) # add user is end of the string by using format