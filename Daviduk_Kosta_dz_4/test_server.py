import unittest
from server import createParser, pars_listen
import argparse


class TestServer(unittest.TestCase):
    def __int__(self):
        self.test_args = None

    def setUp(self):
        test_parser = argparse.ArgumentParser()
        test_parser.add_argument('port', nargs='?', type=int, default=7777)
        test_parser.add_argument('addr', nargs='?', default='127.0.0.1')
        self.test_args = vars(test_parser.parse_args())

    def test_createParser(self):
        parser = createParser()
        args = vars(parser.parse_args())
        self.assertEqual(args, self.test_args)

    def test_pars_listen_OK(self):
        self.assertEqual(pars_listen({"action": "presence"}), {'response': 200, 'alert': 'OK'})

    def test_pars_listen_Bad(self):
        self.assertEqual(pars_listen({"action": ""}), {'response': 400, 'alert': 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
