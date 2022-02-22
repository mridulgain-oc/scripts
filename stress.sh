#!/bin/bash
# running all stress tests from acc-pytest

OUTPUT_PATH=
GIT_BRANCH=kmr2

for i in  test_stress.py test_repeat.py test_stress_2.py test_stress_3.py test_stress_4.py; do
  fname=${i}
  echo "running ${fname}"

sudo docker run --rm --net=host \
  -e PYTHONPATH=/acc-pytests \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/config:/.kube/config \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/:/acc-pytests/tests/input \
  -v /home/noiro/acc-pytests-jobs-config/k8s-bm-1/config/manage.yaml:/acc-pytests/acc_pyutils/pyutils_cfg.yaml \
  noirolabs/acc-pytests:${GIT_BRANCH} python -m pytest -ra -s -rfpesv tests/${fname} | tee ${OUTPUT_PATH}/${fname}.log

done
