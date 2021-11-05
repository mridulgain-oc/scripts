#!/bin/bash
TEST_DIR=.
RES_DIR=/home/noiro/test_results
mkdir $RES_DIR
for i in $(ls $TEST_DIR/test_*.py); do
  echo running $i
  sudo docker run --rm --net=host \
  -e PYTHONPATH=/acc-pytests \
  -v /home/noiro/acc-pytests-jobs-config/fab14/config/config:/.kube/config \
  -v /home/noiro/acc-pytests-jobs-config/fab14/config/:/acc-pytests/tests/input \
  noirolabs/acc-pytests:master-test python -m pytest -s tests/$i | tee ${RES_DIR}/$i.log 
done
