import os
import sys
import logging
from keystoneclient.v2_0 import client as ks_client


class OSUtils(object):
    
    def __init__(self, ks_user, ks_pass, ks_auth_url, ks_tenant_name):
        self.logger = logging.getLogger(__name__)
        self.ks = ks_client.Client(username=ks_user, password = ks_pass, tenant_name = ks_tenant_name, auth_url = ks_auth_url)

    def get_tenants_list(self):
        tenants = self.ks.tenants.list()
        self.logger.info(tenants)
        return tenants
    

