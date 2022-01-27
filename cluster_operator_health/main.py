import os
import pytest
import re
import subprocess

def _get_clusterOperator_states():
    '''
    returns: list of (operator_name, operator_state) tuples
    operator states : {Degraded, Progressing, Available, Upgradeable}
    '''
    p1 = subprocess.Popen(['oc', 'get', 'co'], 
        stdout=subprocess.PIPE, stderr= subprocess.PIPE, encoding='utf-8')
    stdout, stderr = p1.communicate()
    assert p1.returncode == 0, "cmd execution failed: oc get co" # return code check
    data = stdout.split('\n')
    clusterOperators = []
    for line in data[1:-1]:
        line = re.sub(r'\s\s+', ' ', line).split()
        operator_name = line[0]
        operator_state = {
            'Available': line[2],
            'Processing': line[3],
            'Degraded': line[4]
        }
        clusterOperators.append((operator_name, operator_state))
    return clusterOperators


@pytest.mark.parametrize(
    'operator_name, operator_state', _get_clusterOperator_states()
)
def test_isAvailable(operator_name, operator_state):
    assert operator_state['Available'] == 'True', \
        f"ClusterOperator '{operator_name}' is not up"
