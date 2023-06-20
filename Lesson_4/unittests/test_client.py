import unittest

from Lesson_4.client import create_presence, process_ans
from Lesson_4.common.variables import TIME, ACTION, PRESENCE, USER, \
    ACC_NAME, RESPONSE, ERROR


class TestClient(unittest.TestCase):
    def test_presence(self):
        test = create_presence()
        test[TIME] = 0.1

        self.assertEqual(test, {ACTION: PRESENCE, TIME: 0.1, USER: {ACC_NAME: 'Anonim'}})

    def test_ok(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_bad_req(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_resp(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})

# Ran 4 tests in 0.004s
#
# OK
