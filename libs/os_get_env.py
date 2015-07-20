import os
import sys
import logging
from keystoneclient.v2_0 import client as ksc
from gbpclient.v2_0 import client as gbpc

class OSUtils(object):
    
    def __init__(self, ks_user, ks_pass, ks_auth_url, ks_tenant_name):
        self.logger = logging.getLogger(__name__)
        self.ks_user = ks_user
        self.ks_pass = ks_pass
        self.ks_auth_url = ks_auth_url
        self.ks = ksc.Client(username=ks_user, password = ks_pass, tenant_name = ks_tenant_name, auth_url = ks_auth_url)
        self.logger.info('OSUtils intialized successfully')

    def get_gbp_client_by_tenant(self, tenant):
        self.logger.info('get gbpclient object for tenant')
        gbpclient = gbpc.Client(username = self.ks_user, password = self.ks_pass, tenant_name = tenant, auth_url = self.ks_auth_url)
        return gbpclient

    def get_tenants_list(self):
        self.logger.info('Get tenant list from Keystone')
        tenants = self.ks.tenants.list()
        self.logger.info('\n*\n*\t\tTenants\n*\n')
        self.logger.info('*'*50)
        return { tenant.id : tenant.name for tenant in tenants if tenant.enabled and tenant.name != 'services'}
    
    def get_gbp_l3policies_by_tenant(self, tenant):
        gbpclient = self.get_gbp_client_by_tenant(tenant[1])
        l3policies = gbpclient.list_l3_policies()['l3_policies']
        l3policy_list_by_tenant = [ l3p for l3p in l3policies if l3p['tenant_id'] == tenant[0] ]
        self.logger.info('\n*\n*\t\tL3Policies for %s\n*' %(tenant[1]))
        for l3policy in l3policy_list_by_tenant:
            self.logger.info(l3policy['name'])
        return l3policy_list_by_tenant
      

    def get_gbp_l2policies_by_tenant(self, tenant):
        gbpclient = self.get_gbp_client_by_tenant(tenant[1])
        l2policies = gbpclient.list_l2_policies()['l2_policies']
        l2policy_list_by_tenant = [ l2p for l2p in l2policies if l2p['tenant_id'] == tenant[0] ]
        self.logger.info('\n*\n*\t\tL2Policies for %s\n*' %(tenant[1]))
        for l2policy in l2policy_list_by_tenant:
            self.logger.info(l2policy['name'])
        return l2policy_list_by_tenant

    def get_gbp_ptgs_by_tenant(self, tenant):
        gbpclient = self.get_gbp_client_by_tenant(tenant[1])
        ptgs = gbpclient.list_policy_target_groups()['policy_target_groups']
        ptg_list_by_tenant = [ ptg for ptg in ptgs if ptg['tenant_id'] == tenant[0] ]
        self.logger.info('\n*\n*\t\tPolicy Target Groups for %s\n*' %(tenant[1]))
        for ptg in ptg_list_by_tenant:
            self.logger.info(ptg['name'])
        return ptg_list_by_tenant
