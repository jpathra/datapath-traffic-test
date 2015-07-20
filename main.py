import os
import sys
import logging
import logging.config
import datetime
from conf import os_env_conf as os_cfg
from libs import os_get_env as os_lib

logging.config.fileConfig('conf/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler('dptest.log')
#handler.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)
#logger.addHandler(handler)

logger.info('Start the program')
osutils = os_lib.OSUtils(os_cfg.keystone_user, os_cfg.keystone_password, os_cfg.keystone_auth_url, os_cfg.keystone_tenant_name)
tenants = osutils.get_tenants_list()
for tenant in tenants:
    print tenant.name

logger.info('end of main')
