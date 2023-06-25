import unittest
from Lesson_4.common.variables import *
from Lesson_4.server import proc_client_message


class TestServer(unittest.TestCase):
    err_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}

    def test_no_act(self):
        self.assertEqual(proc_client_message({TIME: 0.1, USER: {ACC_NAME: 'Anonim'}}), self.err_dict)

    def test_wrong_act(self):
        self.assertEqual(proc_client_message({ACTION: 'wrong', TIME: 0.1, USER: {ACC_NAME: 'Anonim'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(proc_client_message({ACTION: PRESENCE, USER: {ACC_NAME: 'Anonim'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(proc_client_message({ACTION: PRESENCE, TIME: 0.1}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(proc_client_message({ACTION: PRESENCE, TIME: 0.1, USER: {ACC_NAME: 'Guest'}}), self.err_dict)

    def test_resp_ok(self):
        self.assertEqual(proc_client_message({ACTION: PRESENCE, TIME: 0.1, USER: {ACC_NAME: 'Anonim'}}), self.ok_dict)

# Ran 6 tests in 0.003s
#
# OK
