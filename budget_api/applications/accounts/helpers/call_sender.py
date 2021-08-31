import requests
import decimal


def sender(account, data):
    requests.post('http://172.17.0.1:8001/sender', dict(
        user_id=account.owner.id,
        user_name=account.owner.name,
        user_email=account.owner.email,
        account=account.id,
        value=decimal.Decimal(data['value']),
        operation=data['operation'],
        message='financial account movement'
    ))
