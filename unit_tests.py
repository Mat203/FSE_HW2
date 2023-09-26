import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import last_seen  

class TestLastSeen(unittest.TestCase):
    @patch('requests.get')
    def test_Should_ReturnTestData_When_GetDataCalledWithZero(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'test_data'}
        mock_get.return_value = mock_response

        result = last_seen.get_data(0)
        self.assertEqual(result, 'test_data')

    def test_Should_ReturnCorrectDTAndTZ_When_ParseLastSeenDateCalledWithValidString(self):
        result, tz_info = last_seen.parse_last_seen_date('2023-09-25T17:26:28.123456+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 17, 26, 28, 123456))
        self.assertEqual(tz_info, '+03:00')

    def test_Should_ReturnCorrectDT_When_AdjustTZCalledWithPlusTZ(self):
        dt = datetime(2023, 9, 25, 17, 26, 28)
        result = last_seen.adjust_timezone(dt, '+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 14, 26, 28))

    def test_Should_ReturnCorrectUserNameAndTimeDifference_When_FormatLastSeenCalledWithValidUser(self):
        user = {'nickname': 'test_user', 'lastSeenDate': '2023-09-25T17:26:28.123456+03:00'}
        result_name, result_diff = last_seen.format_last_seen(user)
        self.assertEqual(result_name, 'test_user')
        self.assertTrue(isinstance(result_diff, timedelta))
    
    def test_Should_ReturnJustNow_When_FormatTimeDiffCalledWithTimeDifferenceLessThanThirtySeconds(self):
        diff = timedelta(seconds=29)
        lang = "en-US"
        result = last_seen.format_time_diff(diff,lang)
        self.assertEqual(result, 'was seen just now')

    @patch('builtins.input', return_value='1')
    def test_Should_ReturnEnglish_When_UserChoosesOne(self, mock_input):
        result = last_seen.choose_language()
        self.assertEqual(result, 'en-US')

unittest.main()
