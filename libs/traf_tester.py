import fabric
from fabric.api import *
from fabric.tasks import Task
import os
import sys
import logging

class RemoteUtils(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        env.user = 'root'
        env.password = 'noir0123'
        env.skip_bad_hosts = True
        env.parallel = True
        self.logger.info("RemoteUtils initialized with username and password, running in Fabric parallel mode")


    class setup_env(Task):
        def __init__(self, endpoints):
            self.endpoints = endpoints
            self.logger = logging.getLogger(__name__)
            env.hosts = self.endpoints['dest_eps']
            self.logger.info("Initailized the environment with Endpoints")
        def install_hping(self, environment):
            try:
                out = run("python -c 'import platform; print platform.linux_distribution()[0]'")
                os_info = out
                self.logger.debug("Host %s runs %s" %(env.host_string, os_info))
                if out.return_code == 0:
                    if os_info in ['CentOS', 'Red Hat Enterprise Linux Server', 'Fedora']:
                        out = run("yum -y install hping3")
                        if out.return_code == 0:
                            self.logger.info("Installed hping3 on %s" %(env.host_string))
                    elif os_info in ['Ubuntu']:
                        out = run("apt-get -y install hping3")
                        if out.return_code == 0:
                            self.logger.info("Installed hping3 on %s" %(env.host_string))
            except SystemExit,e:
                self.logger.warn("Exception while executing task: %s", str(e))          

        def test_ping(self, environment, contract):
            try:
                for dest_ep in self.endpoints['dest_eps']:
                    if dest_ep != env.host_string:
                        out = run("hping3 %s --icmp -c 10 --fast -q" %(dest_ep))
                        print str(out).split("\n")[-2]
            except SystemExit,e:
                self.logger.warn("Exception while executing task: %s", str(e))
        
        def test_tcp(self,environment, contract):
            pass

        def test_udp(self, environment, contract):
            pass
             
    
    def start_task(self, endpoints):
        prep = self.setup_env(endpoints)
#        fabric.tasks.execute(prep.install_hping, env)
        for contract in endpoints['contract']:
            if contract['protocol'] == 'icmp':
                fabric.tasks.execute(prep.test_ping, env, contract)
            if contract['protocol'] == 'tcp':
                fabric.tasks.execute(prep.test_tcp, env, contract)
            if contract['protocol'] == 'udp':
                fabric.tasks.execute(prep.test_udp, env, contract)

if __name__ == '__main__':
    rm = RemoteUtils()
    rm.start_task()
    
