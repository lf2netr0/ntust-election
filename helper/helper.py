
def hasher(str):
    from hashlib import md5
    m = md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()
def error_response(error):
    import datetime
    import json
    return json.dumps({'status':'error','data':error,'time':str(datetime.datetime.now())},ensure_ascii=False)

def success_response(data):
    import datetime
    import json
    return json.dumps({'status':'success', 'data':data, 'time':str(datetime.datetime.now())})

def encrypt(string, pubkeys = []):
    import pickle
    import rsa
    from pyaes import AESModeOfOperationCTR

    first_key = rsa.PublicKey.load_pkcs1_openssl_pem(open(pubkey_path(pubkeys[0])).read().encode('utf8'))
    content = rsa.encrypt(string.encode('utf8'), first_key)

    aes_key = rsa.randnum.read_random_bits(128)
    aes = AESModeOfOperationCTR(aes_key)

    encrypted_content = aes.encrypt(content)
    second_key = rsa.PublicKey.load_pkcs1_openssl_pem(open(pubkey_path(pubkeys[1])).read().encode('utf8'))
    encrypted_aes_key = rsa.encrypt(aes_key, second_key)

    return pickle.dumps({
        'key': pubkeys,
        'content': encrypted_content,
        'aes_key': encrypted_aes_key
    })

def decrypt(data = ''):
    import pickle
    import rsa
    from pyaes import AESModeOfOperationCTR

    data = pickle.loads(data)

    first_key = rsa.PrivateKey.load_pkcs1(open(prikey_path(data['key'][1])).read().encode('utf8'))
    aes_key = rsa.decrypt(data['aes_key'], first_key)

    aes = AESModeOfOperationCTR(aes_key)
    content = aes.decrypt(data['content'])

    second_key = rsa.PrivateKey.load_pkcs1(open(prikey_path(data['key'][0])).read().encode('utf8'))
    
    return rsa.decrypt(content, second_key).decode('utf8')

def path(file_name):
    from os import path
    return path.join(path.dirname(path.realpath(__file__)), '..', file_name)

def prikey_path(file_name):
    return path('public_key/' + file_name + '.private.pem')

def pubkey_path(file_name):
    return path('public_key/' + file_name + '.public.pem')

def send_mail(to,url,key,content):
    import requests
    return requests.post(
        url + '/messages',
        auth=("api", key),
        data={"from": "NTUST Vote <no-reply@ntust.me>",
              "to": [to],
              "subject": "台科大學生會電子投票",
              "html": content})