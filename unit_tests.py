import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import last_seen

class TestGetData(unittest.TestCase):
    @patch('requests.get')
    def test_Should_ReturnTestData_When_GetDataCalledWithZero(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'test_data'}
        mock_get.return_value = mock_response

        result = last_seen.get_data(0)
        self.assertEqual(result, 'test_data')

class TestParseLastSeenDate(unittest.TestCase):
    def test_Should_ReturnCorrectDTAndTZ_When_ParseLastSeenDateCalledWithValidString(self):
        result, tz_info = last_seen.parse_last_seen_date('2023-09-25T17:26:28.12345678+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 17, 26, 28, 123456))
        self.assertEqual(tz_info, '+03:00')

class TestAdjustTimezone(unittest.TestCase):
    def test_Should_ReturnCorrectDT_When_AdjustTZCalledWithPlusTZ(self):
        dt = datetime(2023, 9, 25, 17, 26, 28)
        result = last_seen.adjust_timezone(dt, '+03:00')
        self.assertEqual(result, datetime(2023, 9, 25, 14, 26, 28))

class TestFormatLastSeen(unittest.TestCase):
    def test_Should_ReturnCorrectUserNameAndTimeDifference_When_FormatLastSeenCalledWithValidUser(self):
        user = {'nickname': 'test_user', 'lastSeenDate': '2023-09-25T17:26:28.123456+03:00'}
        result_name, result_diff = last_seen.format_last_seen(user)
        self.assertEqual(result_name, 'test_user')
        self.assertTrue(isinstance(result_diff, timedelta))


class TestFormatTimeDiff(unittest.TestCase):
    def test_Should_ReturnJustNow_When_FormatTimeDiffCalledWithTimeDifferenceLessThanThirtySeconds(self):
        diff = timedelta(seconds=29)
        lang = "en-US"
        result = last_seen.format_time_diff(diff,lang)
        self.assertEqual(result, 'was seen just now')

    def test_Should_ReturnLessThanAMinuteAgo_When_FormatTimeDiffCalledWithTimeDifferenceLessThanSixtySeconds(self):
        diff = timedelta(seconds=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen less than a minute ago')

    def test_Should_ReturnCoupleOfMinutesAgo_When_FormatTimeDiffCalledWithTimeDifferenceLessThanAnHour(self):
        diff = timedelta(minutes=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen a couple of minutes ago')

    def test_Should_ReturnAnHourAgo_When_FormatTimeDiffCalledWithTimeDifferenceLessThanTwoHours(self):
        diff = timedelta(hours=1, minutes=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen an hour ago')

    def test_Should_ReturnToday_When_FormatTimeDiffCalledWithTimeDifferenceLessThanADay(self):
        diff = timedelta(hours=23, minutes=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen today')

    def test_Should_ReturnYesterday_When_FormatTimeDiffCalledWithTimeDifferenceLessThanTwoDays(self):
        diff = timedelta(days=1, hours=23, minutes=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen yesterday')

    def test_Should_ReturnThisWeek_When_FormatTimeDiffCalledWithTimeDifferenceLessThanAWeek(self):
        diff = timedelta(days=6, hours=23, minutes=59)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen this week')
    def test_Should_ReturnLongTimeAgo_When_FormatTimeDiffCalledWithTimeDifferenceMoreThanAWeek(self):
        diff = timedelta(days=7)
        lang = "en-US"
        result = last_seen.format_time_diff(diff, lang)
        self.assertEqual(result, 'was seen long time ago')
    
class TestChooseLanguage(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_Should_ReturnEnglish_When_UserChoosesOne(self, mock_input):
        result = last_seen.choose_language()
        self.assertEqual(result, 'en-US')

    @patch('builtins.input', return_value='2')
    def test_Should_ReturnUkrainian_When_UserChoosesTwo(self, mock_input):
        result = last_seen.choose_language()
        self.assertEqual(result, 'uk-UA')

class TestGetAllData(unittest.TestCase):
    @patch('last_seen.get_data')
    def test_Should_ReturnAllData_When_GetAllDataCalled(self, mock_get_data):
        mock_get_data.side_effect = [['data1', 'data2'], []]
        result = last_seen.get_all_data()
        self.assertEqual(result, ['data1', 'data2'])

class TestPrintUserStatus(unittest.TestCase):
    @patch('builtins.print')
    def test_Should_PrintCorrectStatus_When_PrintUserStatusCalledWithValidData(self, mock_print):
        user_name = 'test_user'
        status = 'was seen just now'
        last_seen.print_user_status(user_name, status)
        mock_print.assert_called_once_with(f'{user_name} {status}')

unittest.main()