import argparse
import yaml
from acc_pyutils.api import KubeAPI
from tests import lib

KAPI = KubeAPI()

parser = argparse.ArgumentParser()
parser.add_argument('-ns', '--namespace', default='default', help='name space name')
parser.add_argument('-svc', '--service', default='nginx-service', help='service name')
parser.add_argument('-deploy', '--deployment', default='nginx-deploy', help='service endpoints')

args = parser.parse_args()
ns = args.namespace
svc_name = args.service
deploy_name = args.deployment

# ns = 'dummy-ns-1'
# svc_name = 'nginx-service-1'
# deploy_name = 'dummy-nginx-deploy-1'
# snatpol_name will be derived frm service

deploy = KAPI.get_detail('deployment', name = deploy_name, namespace=ns)
deploy_manifest_file = '/tmp/depl.yaml'
with (open(deploy_manifest_file,'w')) as f:
    yaml.dump(deploy, f)

svc_detail= KAPI.get_detail('svc', name = svc_name, namespace=ns)
# print(svc_detail)
snat_ips = list()
for ip_detail in svc_detail['status']['loadBalancer']['ingress']:
    snat_ips.append(ip_detail['ip'])
print(snat_ips)
_, labels, _, _ = lib.get_deployment_details(name=deploy_name, namespace=ns)
# print(labels)
kwargs = {'labels': ','.join(labels)}
pods = KAPI.get_detail('pod', namespace=ns, **kwargs)

while True:
    for pod in pods['items']:
        print(pod['metadata']['name'])
        lib.validate_traffic(
            deploy_manifest_file, pod['metadata']['name'], snat_ips[0], namespace=ns)
