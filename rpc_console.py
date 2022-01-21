import time
from rchain.crypto import PrivateKey
from rchain.client import RClient

if __name__ == '__main__':
    private = PrivateKey.from_hex('9258e9591e649b465c92136df451be6bd025ba97a4b8180631cae6c5f2e84723')
    valid_after_block_no = 10
    host = '127.0.0.1'

    client = RClient(host, 40401)
    sig = None

    while True:
        command = input('> ')

        if command.startswith('deploy'):
            contract = command.replace('deploy ', '')
            print(contract)
            sig = client.deploy(private, contract, 1, 100000, valid_after_block_no, int(time.time() * 1000))
            print(sig)
        elif command.startswith('valid_after_block_no'):
            _, no = command.split()
            valid_after_block_no = int(no)
        elif command.startswith('propose'):
            admin_client = RClient(host, 40402)
            print(admin_client.propose())
        elif command.startswith('result'):
            data = client.get_data_at_deploy_id(sig, 1)
            print(data)
        elif command.startswith('exit'):
            break
