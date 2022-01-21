import requests
import base64
from rchain.crypto import PrivateKey
from rchain.util import create_deploy_data
import time


def create_deploy(contract: str, private, phlo_price=1, valid_after_block_no=0):
    return create_deploy_data(key=private,
                              term=contract, phlo_price=phlo_price,
                              phlo_limit=100000,
                              valid_after_block_no=valid_after_block_no,
                              timestamp_millis=int(time.time() * 1000))


def send_deploy(deploy_data):
    json = {
        'data': {
            'term': deploy_data.term,
            'timestamp': deploy_data.timestamp,
            'phloPrice': deploy_data.phloPrice,
            'phloLimit': deploy_data.phloLimit,
            'validAfterBlockNumber': deploy_data.validAfterBlockNumber
        },
        'sigAlgorithm': deploy_data.sigAlgorithm,
        'signature': base64.b16encode(deploy_data.sig),
        'deployer': base64.b16encode(deploy_data.deployer)
    }
    return requests.post('http://localhost:40403/api/deploy', json=json)


def propose():
    return requests.post('http://localhost:40405/api/propose')


def get_result(sig: str):
    json = {'depth': 1, 'name': {'UnforgDeploy': {'data': sig}}}
    return requests.post('http://localhost:40403/api/data-at-name', json=json)


def get_result_at_par(sig: str, block_hash: str, use_pre_state_hash: bool = False):
    json = {
        'blockHash': block_hash,
        'name': {
            'UnforgDeploy': {
                'data': sig
            }
        },
        'usePreStateHash': use_pre_state_hash
    }
    return requests.post('http://localhost:40403/api/data-at-par', json=json)


if __name__ == '__main__':

    private = PrivateKey.from_hex('9258e9591e649b465c92136df451be6bd025ba97a4b8180631cae6c5f2e84723')
    valid_after_block_no = 10
    deploy_data = None

    while True:
        command = input('> ')

        if command.startswith('deploy'):
            contract = command.replace('deploy ', '')
            print(contract)
            phlo_price, valid = [int(item) for item in input('phlo price, valid after: ').split()]
            deploy_data = create_deploy(contract, private, phlo_price, valid)

            # for i in range(1000):
            ans = send_deploy(deploy_data)
            print(ans.text)
        elif command.startswith('valid_after_block_no'):
            _, no = command.split()
            valid_after_block_no = int(no)
        elif command.startswith('propose'):
            ans = propose()
            print(ans.text)
        elif command.startswith('at_name'):
            ans = get_result(base64.b16encode(deploy_data.sig))
            print(ans.text)
        elif command.startswith('at_par'):
            block_hash = input('block hash: ')
            ans = get_result_at_par(base64.b16encode(deploy_data.sig), block_hash)
            print(ans.text)
        elif command.startswith('exit'):
            break
