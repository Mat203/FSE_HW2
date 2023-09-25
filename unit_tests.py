import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import last_seen  

class TestYourModule(unittest.TestCase):
    @patch('requests.get')
    def Should_ReturnTestData_When_GetDataCalledWithZero(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'test_data'}
        mock_get.return_value = mock_response

        result = last_seen.get_data(0)
        self.assertEqual(result, 'test_data')

    def Should_ReturnCorrectDTAndTZ_When_ParseLastSeenDateCalledWithValidString(self):
        result, tz_info = last_seen.parse_last_seen_date('2023-09-25T17:26:28.123456+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 17, 26, 28, 123456))
        self.assertEqual(tz_info, '+03:00')

    def Should_ReturnCorrectDT_When_AdjustTZCalledWithPlusTZ(self):
        dt = datetime(2023, 9, 25, 17, 26, 28)
        result = last_seen.adjust_timezone(dt, '+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 14, 26, 28))

    def Should_ReturnCorrectUserNameAndTimeDifference_When_FormatLastSeenCalledWithValidUser(self):
        user = {'nickname': 'test_user', 'lastSeenDate': '2023-09-25T17:26:28.123456+03:00'}
        result_name, result_diff = last_seen.format_last_seen(user)
        self.assertEqual(result_name, 'test_user')
        self.assertTrue(isinstance(result_diff, timedelta))

    def Should_ReturnJustNow_When_FormatTimeDiffCalledWithTimeDifferenceLessThanThirtySeconds(self):
        diff = timedelta(seconds=29)
        result = last_seen.format_time_diff(diff)
        self.assertEqual(result, 'just now')

if __name__ == '__main__':
    unittest.main()
