import unittest
import time
import json
from my_func import js_dec, js_enc


# python3 test_my_func.py

class TestMyFunc(unittest.TestCase):

    def test_js_dec(self):
        with open('data.json') as f:
            objects = json.loads(f.read())
            json_data = json.dumps(objects)
            enc_data = json_data.encode('utf-8')
        self.assertEqual(js_dec(enc_data), objects)

    def test_js_enc(self):
        with open('data.json') as f:
            objects = json.loads(f.read())
            json_data = json.dumps(objects)
            enc_data = json_data.encode('utf-8')
        self.assertEqual(js_enc(objects), enc_data)


if __name__ == '__main__':
    unittest.main()
