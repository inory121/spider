import unittest


class TestUnit(unittest.TestCase):

    def test_ex(self):
        try:
            i = 1/0
        except BaseException as e:
            print(e)
            print("111")
