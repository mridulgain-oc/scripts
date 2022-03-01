import os, yaml

RESOURCE_SET=2 # each set contains a namespace, an snatpolicy, an ngnix deployment & a service
REPLICAS=1 # no of pods per deployment or, no of endpoints per service
# OUTPUT_PATH = './yamls'
OUTPUT_FILE = 'resources.yaml'
IDENTIFIER_PREFIX = 'dummy-'
IP_PREFIX = '151.20.1.'
MANIFEST_BASE = '''
---
apiVersion: v1
kind: Namespace
metadata:
  name: dummy-ns-
---
apiVersion: aci.snat/v1
kind: SnatPolicy
metadata:
  name: dummy-snatpolicy-
spec:
  snatIp:
    -  151.20.1.
  selector:
    namespace: dummy-ns-
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dummy-nginx-deploy-
  namespace: dummy-ns-
spec:
  selector:
    matchLabels:
      name: dummy-resource-
  replicas: 1
  template:
    metadata:
      labels:
        name: dummy-resource-
    spec:
      containers:
      - name: nginx
        image: noiro-quay.cisco.com/noiro/nginx-non-root:un
        ports:
        - containerPort: 8080
        imagePullPolicy: IfNotPresent
    #   nodeSelector:
    #    kubernetes.io/hostname: openupi-nchx2-worker-0-djc2h

---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service-
  namespace: dummy-ns-
spec:
  selector:
    name: dummy-resource-
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
  type: LoadBalancer
'''
out = []
for i in range(1, RESOURCE_SET+1):
    i = str(i)
    # yamls = yaml.safe_load_all(open('resources.yaml','r'))
    yamls = yaml.safe_load_all(MANIFEST_BASE)
    yamls = list(yamls) # generator to list

    # ns = yamls.__next__()
    ns_name = IDENTIFIER_PREFIX + "ns-" + i
    ns = yamls[0]
    ns['metadata']['name'] = ns_name
    # ns.dump(f"ns-{i}.yaml")

    # snat = yamls.__next__()
    snat_name = IDENTIFIER_PREFIX + "snatpolicy-" + i
    snat_ip = IP_PREFIX + i
    snat = yamls[1]
    snat['metadata']['name'] = snat_name
    snat['spec']['selector']['namespace'] = ns_name
    snat['spec']['snatIp'][0] = snat_ip

    # deploy = yamls.__next__()
    deploy_name = IDENTIFIER_PREFIX + "ngnix-deployment-" + i
    selector_name = IDENTIFIER_PREFIX + "resource-" + i
    deploy = yamls[2]
    deploy['metadata']['name'] = deploy_name
    deploy['metadata']['namespace'] = ns_name
    deploy['spec']['replicas'] = REPLICAS
    deploy['spec']['selector']['matchLabels']['name'] = selector_name
    deploy['spec']['template']['metadata']['labels']['name'] = selector_name

    # svc = yamls.__next__()
    svc_name = IDENTIFIER_PREFIX + "nginx-svc-" + i
    svc = yamls[3]
    svc['metadata']['name'] = svc_name
    svc['metadata']['namespace'] = ns_name
    svc['spec']['selector']['name'] = selector_name

    out.extend(yamls)
    # fout = os.path.join(OUTPUT_PATH, f"resources-{i}.yaml")
print(OUTPUT_FILE)
with (open(OUTPUT_FILE,'w')) as f:
    yaml.dump_all(out, f)
