#!/bin/bash
i=0
while true
do
        host_pods=$(kubectl get po -n aci-containers-system  | grep -i host | awk '{ print $1 }')
        for po in $host_pods
        do
                echo "checking " $po
                race=$(kubectl logs -n aci-containers-system $po -c aci-containers-host --previous | grep -iw race)
                if [[ ! -z "$race" ]]
                then
            echo $po: $race
                        kubectl logs -n aci-containers-system $po -c aci-containers-host --previous > $po-$i.log
                fi
        #echo deleting: $po
        #kubectl delete po -n aci-containers-system $po > /dev/null
        done

        ctrl_pods=$(kubectl get po -n aci-containers-system  | grep -i controller | awk '{ print $1 }')
        for po in $ctrl_pods
        do
              race=$(kubectl logs -n aci-containers-system $po  | grep -iw race)
              if [[ ! -z "$race" ]]
              then
           echo $po: $race
                      kubectl logs -n aci-containers-system $po > $po-$i.log
              fi
        done
    i=$((i+1))
        sleep 300
done
