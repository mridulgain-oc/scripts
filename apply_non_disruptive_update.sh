#!/bin/bash
for node in $(oc get node -o name)
do
    node=($(echo $node | tr "/" " "))
    node=${node[1]}
    oc adm drain $node --force --delete-emptydir-data --ignore-daemonsets
    for i in $(oc -n aci-containers-system get pod -o wide | grep $node | awk '{print $1}'); do
        oc -n aci-containers-system delete po $i
    done
    sleep 5
    kubectl uncordon $node
done
