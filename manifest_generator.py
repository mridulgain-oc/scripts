import os, yaml

RESOURCE_SET=1 # each set contains a namespace, an snatpolicy, a deployment & a service
OUTPUT_PATH = './yamls'
REPLICAS=50
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
      nodeSelector:
       kubernetes.io/hostname: openupi-nchx2-worker-0-djc2h

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
try:
    os.mkdir(OUTPUT_PATH)
except FileExistsError:
    pass

for i in range(1, RESOURCE_SET+1):
    i = str(i)
    # yamls = yaml.safe_load_all(open('resources.yaml','r'))
    yamls = yaml.safe_load_all(MANIFEST_BASE)
    yamls = list(yamls) # generator to list

    # ns = yamls.__next__()
    ns = yamls[0]
    ns['metadata']['name'] += i
    # ns.dump(f"ns-{i}.yaml")

    # snat = yamls.__next__()
    snat = yamls[1]
    snat['metadata']['name'] += i
    snat['spec']['selector']['namespace'] += i
    snat['spec']['snatIp'][0] += i

    # deploy = yamls.__next__()
    deploy = yamls[2]
    deploy['metadata']['name'] += i
    deploy['metadata']['namespace'] += i
    deploy['spec']['replicas'] = REPLICAS
    deploy['spec']['selector']['matchLabels']['name'] += i
    deploy['spec']['template']['metadata']['labels']['name'] += i

    # svc = yamls.__next__()
    svc = yamls[3]
    svc['metadata']['name'] += i
    svc['metadata']['namespace'] += i
    svc['spec']['selector']['name'] += i

    fout = os.path.join(OUTPUT_PATH, f"resources-{i}.yaml")
    print(fout)
    with (open(fout,'w')) as f:
        yaml.dump_all(yamls, f)
