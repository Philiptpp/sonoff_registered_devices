import time, hmac, hashlib, random, base64, json, requests, uuid, string
from http import HTTPStatus


def create_signature(credentials):
    app_details = {
        'email': credentials['email'],
        'password': credentials['password'],
        'version': '6',
        'ts': int(time.time()),
        'nonce': ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)),
        'appid': 'R8Oq3y0eSZSYdKccHlrQzT1ACCOUT9Gv',
        'imei': credentials['imei'],
        'os': 'iOS',
        'model': 'iPhone11,8',
        'romVersion': '13.2',
        'appVersion': '3.11.0'
    }
    decryptedAppSecret = b'1ve5Qk9GXfUhKAn1svnKwpAlxXkMarru'
    hex_dig = hmac.new(
        decryptedAppSecret,
        str.encode(json.dumps(app_details)),
        digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hex_dig).decode()
    return (sign, app_details)


def login(credentials, api_region='us'):
    sign, payload = create_signature(credentials)
    headers = {
        'Authorization' : 'Sign ' + sign,
        'Content-Type'  : 'application/json;charset=UTF-8'
    }

    r = requests.post('https://{}-api.coolkit.cc:8080/api/user/login'.format(api_region),
        headers=headers, json=payload)

    if not (r.status_code == HTTPStatus.OK):
        return ({"error": "Unable to access coolkit api server [{}]".format(r.text)})

    resp = r.json()
    if 'error' in resp and 'region' in resp and resp['error'] == HTTPStatus.MOVED_PERMANENTLY:
        api_region = resp['region']
        print('API region set to: {}'.format(api_region))
        return login(credentials, api_region)

    return {"response": resp, "region": api_region, "imei": credentials['imei']}


def list_devices(user_info, attempt=1):
    headers = {
        'Authorization' : 'Bearer ' + user_info['response']['at'],
        'Content-Type'  : 'application/json;charset=UTF-8'
    }

    r = requests.get('https://{}-api.coolkit.cc:8080/api/user/device?lang=en&apiKey={}&getTags=1&version=6&ts=%s&nonce=%s&appid=oeVkj2lYFGnJu5XUtWisfW4utiN4u9Mq&imei=%s&os=iOS&model=%s&romVersion=%s&appVersion=%s'.format(
            user_info['region'], user_info['response']['user']['apikey'], str(int(time.time())), ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)), user_info['imei'], 'iPhone10,6', '11.1.2', '3.5.3'), headers=headers)

    resp = r.json()
    if 'error' in resp and resp['error'] in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED]:
        if (attempt == 5):
            print("Unable to fetch devices, please close eWelink application across all devices and try again.")
            return None
        return list_devices(user_info, attempt+1)

    return resp['devicelist']


if __name__ == '__main__':
    print('eWelink Credentials')
    print('-------------------')
    email = input("eWelink registered email: ")
    password = input("eWelink password: ")
    print('\n')

    user_info = login({
        'email': email,
        'password': password,
		'imei': str(uuid.uuid4())
        })
    
    if 'at' not in user_info['response']:
        print("Login failed! Please check credentials!")

    else:
        devices = list_devices(user_info)
        print('Found {} devices registered to this account'.format(len(devices)))
        print('\nAPI Key: {}\n'.format(user_info['response']['user']['apikey']))
        if len(devices):
            print('{:10} {:10} : {:40} [{:10}]  {}'.format('Brand', 'Model', 'Device Name', 'Device ID', 'Device API Key'))
            print('{:10} {:10} : {:40}  {:11}  {}'.format('=====', '=====', '===========', '=========', '=============='))
            for device in devices:
                print('{:10} {:10} : {:40} [{:10}] {}'.format(device['brandName'], device['productModel'], device['name'], device['deviceid'], device['devicekey']))
