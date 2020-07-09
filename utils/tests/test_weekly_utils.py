''' Module to run unit tests for weekly utils module '''

import pytest
import unittest

from weekly_utils import weekly_utils

# todo: implement tests for weekly_utils
class GetWeekEndTestCase(unittest.TestCase):

    def test_valid_week_start(self):
        ''' Test that the correct week end date is returned from get_week_end '''

        week_start = "2020-07-06"
        result = get_week_end(week_start)
        expected = "2020-07-12"

        self.assertEqual(result, expected)

    def test_invalid_str_format(self):
        ''' Test that given an invalid string an IncorrectFormat exception is raised '''

        week_start = "06/07/2020"
        self.assertRaises(IncorrectFormatException, get_week_end, week_start)
