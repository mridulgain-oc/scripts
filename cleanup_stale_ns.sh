#!/bin/bash

for i in $(oc get ns -o name | grep -i terminating)
do
i=($(echo $i | tr "/" " "))
i=${i[1]}
kubectl get ns $i -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/$i/finalize -f -
done
