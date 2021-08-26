import datetime, requests, json


# Get access token
def get_access_token(host):
    token = requests.get(url=f'{host}/auth/signin', headers={
        'Authorization': 'Basic dXNlcjpwYXNzd29yZA=='
    }).json()['data']['tokens']['access']
    return token


# Get x-operation-id
def get_x_operation_id(token, host):
    x_operation_id = requests.post(url=f'{host}/operations', headers={
        'Authorization': f'Bearer {token}'
    }).json()['data']['operationId']
    return x_operation_id


# Get message from Kafka
def get_message_from_kafka(operation_id):
    kafka_host = 'http://82.144.223.29:5000'
    kafka_message = requests.get(
        url=kafka_host + '/x-operation-id/' + operation_id
    )
    if kafka_message.status_code == 404:
        date = datetime.datetime.now()
        date_new = datetime.datetime.now() + datetime.timedelta(seconds=25)
        while date < date_new:
            kafka_message = requests.get(
                url=kafka_host + '/x-operation-id/' + operation_id
            )
            date = datetime.datetime.now()
            if kafka_message.status_code == 200:
                kafka_message = requests.get(
                    url=kafka_host + '/x-operation-id/' + operation_id
                ).json()
                del kafka_message['_id']
                return kafka_message
        print('The message was not found in Kafka topic')
    if kafka_message.status_code == 200:
        kafka_message = requests.get(
            url=kafka_host + '/x-operation-id/' + operation_id
        ).json()
    del kafka_message['_id']
    return kafka_message


# Create EI
def create_ei_env(host, token, x_operation_id, payload):
    requests.post(url=f'{host}/do/ei?country=MD&lang=ro', headers={
        'Authorization': f'Bearer {token}',
        'X-OPERATION-ID': x_operation_id,
        'Content-Type': 'application/json'
    }, data=json.dumps(payload))
    kafka_message = get_message_from_kafka(x_operation_id)
    if 'errors' in kafka_message:
        return kafka_message
    else:
        ei_cpid = kafka_message['data']['ocid']
        return ei_cpid


# Get release
def get_ei_release(host, cpid):
    public_point = ''
    if host == 'http://10.0.20.126:8900/api/v1':
        public_point = 'http://dev.public.eprocurement.systems/budgets/'
    if host == 'http://10.0.10.116:8900/api/v1':
        public_point = 'http://public.eprocurement.systems/budgets/'

    url = f'{public_point}{cpid}'
    public_point_data = requests.get(url=url).json()
    return public_point_data
