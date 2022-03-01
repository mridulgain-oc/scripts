 
# How to run 
- Download snat_traffic_monitor.py on any lab say, k8s-bm-1
- create some test resources with  
`oc apply -f https://raw.githubusercontent.com/mridulgain-oc/scripts/main/snat_traffic_monitor/test_resources.yaml`  
- Run the script by mounting on acc-pytests image;  
```
sudo docker run --rm --net=host \
  -e PYTHONPATH=/acc-pytests \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/config:/.kube/config \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/:/acc-pytests/tests/input \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/manage.yaml:/acc-pytests/acc_pyutils/pyutils_cfg.yaml \
  -v /home/noiro/Downloads/continuous_snat_traffic_monitor.py:/acc-pytests/scripts/continuous_snat_traffic_monitor.py \
  noirolabs/acc-pytests:kmr2 python  -m scripts.continuous_snat_traffic_monitor -ns dummy-ns-1 -svc nginx-service-1 -deploy dummy-nginx-deploy-1
```
- Now while the script is running delete the snat policy (`oc delete snatpolicy dummy-snatpolicy-1 -n dummy-ns-1`). The script will get stuck and get timeout (after 120 sec according to default settings)
