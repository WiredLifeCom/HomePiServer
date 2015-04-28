__author__ = 'J'
import unittest
import Main


class UserData:
    def __init__(self):
        self.userName = 'Hassan'


class TestObjectMethod(unittest.TestCase):

    def test_NotEqual_Encode(self):
        testObject = UserData
        dataObject = Main.UserData()
        encoder = Main.JsonEncoder(testObject)
        result = "Hassan"

        self.assertNotEqual(encoder.Encode(), result)
        print result

if __name__ == '__main__':
    unittest.main()
