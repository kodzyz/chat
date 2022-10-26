import json


def js_dec(data):
    dec_data = data.decode('utf-8')
    js_data = json.loads(dec_data)
    return js_data


def js_enc(data):
    js_data = json.dumps(data)
    enc_data = js_data.encode('utf-8')
    return enc_data


