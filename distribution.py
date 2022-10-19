from web3 import Web3
from eth_account import Account
import config

connection = Web3(Web3.HTTPProvider(config.rpc_url))

if connection.isConnected():
    print('connection to the network is successful')
else:
    raise (ConnectionError, "try to change rpc url")

file = open('accounts.txt', 'a')
created_accounts = []
for i in range(config.number_of_accounts):
    new_account = Account.create()
    created_accounts.append(new_account)
    file.write(new_account.privateKey.hex() + '\n')
    print(f'Account #{i + 1}\naddress: {new_account.address}\nprivate key: {new_account.privateKey.hex()}\n')
file.close()

my_account = connection.eth.account.from_key(config.my_private_key)
my_address = my_account.address
transaction_count = connection.eth.getTransactionCount(my_address)

for created_account in created_accounts:
    print(f'{config.amount_to_send} -> {created_account.address}')

    transaction = {
        'chainId': connection.eth.chain_id,
        'from': my_address,
        'to': created_account.address,
        'value': int(Web3.toWei(config.amount_to_send, 'ether')),
        'nonce': transaction_count,
        'gasPrice': connection.eth.gas_price,
        'gas': 2_000_000,
    }
    transaction_count += 1

    signed_txn = connection.eth.account.sign_transaction(transaction, config.my_private_key)
    txn_hash = connection.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f'txn hash: {txn_hash.hex()}\n')
