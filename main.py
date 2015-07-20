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
def main():
    print 'I am here'
    logger.info('Start the program')
    logger.info('Initialize OSUtils')

    osutils = os_lib.OSUtils(os_cfg.keystone_user, os_cfg.keystone_password, os_cfg.keystone_auth_url, os_cfg.keystone_tenant_name)
    logger.info('Get tenant details')
    tenants = osutils.get_tenants_list()
    logger.info('Get GBP L3 policies per tenant')
    for tenant in tenants.items(): 
        osutils.get_gbp_l3policies_by_tenant(tenant)
        osutils.get_gbp_l2policies_by_tenant(tenant)
        osutils.get_gbp_ptgs_by_tenant(tenant)
    logger.info('end of main')

main()
