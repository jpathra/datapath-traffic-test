import os
import sys
import logging
import logging.config
import datetime
from conf import os_env_conf as os_cfg
from libs import os_get_env as os_lib
from libs import traf_tester as remote_libs

logging.config.fileConfig('conf/logging.ini')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
def main():
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
    
    ip_list = ['10.30.120.45', '10.30.120.46']
    contract = [{'name': 'allow_ssh', 'protocol' : 'tcp', 'port' : 22, 'direction' : 'in', 'action' : 'allow'}, {'name': 'allow_icmp', 'protocol' : 'icmp', 'port' : 'None', 'direction' : 'in', 'action' : 'allow'}]
    endpoints = { 'src_tenant' : 'dummy_tenant',
                  'dest_tenant' : 'dummy_tenant',
                  'src_grp' : 'dummy_group',
                  'dest_grp' : 'dummy_group',
                  'src_eps' : ip_list,
                  'dest_eps' : ip_list,
                  'contract' : contract
                }

    remote = remote_libs.RemoteUtils()
    remote.start_task(endpoints)

if __name__ == '__main__':
    main()
