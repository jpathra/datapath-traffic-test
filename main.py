import os
import sys
import logging
import datetime
from conf import os_env_conf as os_cfg
from libs import os_get_env as os_lib

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info('Start the program')
os_lib.keystone_auth()
print os_cfg.keystone_auth_url
