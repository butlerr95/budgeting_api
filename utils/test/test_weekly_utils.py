''' Module to run unit tests for weekly utils module '''

import pytest
import unittest

from utils import *

class GetWeekEndTestCase(unittest.TestCase):
    ''' Tests for the get_week_end method '''

    def test_valid_week_start(self):
        ''' Test that the correct week end date is returned from get_week_end '''

        week_start = "2020-07-06"
        result = get_week_end(week_start)
        expected = "2020-07-12"

        self.assertEqual(result, expected)

    def test_invalid_str_format(self):
        ''' Test that given an invalid string an IncorrectFormat exception is raised '''

        week_start = "06/07/2020"
        self.assertRaises(IncorrectDateFormatException, get_week_end, week_start)

class CalculateWeeklyBudgetTestCase(unittest.TestCase):
    ''' Tests for the calculate_weekly_budget method '''

    def setUp(self):
        ''' Set up before each test method is run '''
        self.week_start = "2020-07-06"
        self.week_end = "2020-07-12"
        self.budgets = [{"end_date": "2099-01-01", "amount": 100}]

    def test_single_budget(self):
        ''' Test that correct result is obtained with a single budget for the week '''
        result = calculate_weekly_budget(self.week_start, self.week_end, self.budgets)
        
        expected = 23.07

        self.assertEqual(result, expected)

    def test_two_budgets(self):
        ''' Test that correct result is obtained with 2 budgets for the week '''
        self.budgets = [{"end_date": "2020-07-08", "amount": 100},
                    {"end_date": "2099-01-01", "amount": 200}]
        result = calculate_weekly_budget(self.week_start, self.week_end, self.budgets)
        
        expected = 36.26

        self.assertEqual(result, expected)

    def test_multi_budget(self):
        ''' Test that correct result is obtained with multiple budgets for the week '''
        self.budgets = [{"end_date": "2020-07-07", "amount": 100},
                    {"end_date": "2020-07-08", "amount": 200},
                    {"end_date": "2020-07-10", "amount": 300},
                    {"end_date": "2020-07-12", "amount": 400}]
        result = calculate_weekly_budget(self.week_start, self.week_end, self.budgets)
        
        expected = 59.34

        self.assertEqual(result, expected)

    def test_incorrect_week_start_end_format_single_budget(self):
        ''' Test that the correct exception is raised when an incorrect string is passed '''
        self.week_start = ""
        self.week_end = ""
        budgets = [{"end_date": "2020-07-07", "amount": 100}]

        result = calculate_weekly_budget(self.week_start, self.week_end, self.budgets)
        
        expected = 23.07

        self.assertEqual(result, expected)

    def test_incorrect_week_start_end_format_multi_budget(self):
        ''' Test that the correct exception is raised when an incorrect string is passed '''
        self.week_start = ""
        self.week_end = ""
        self.budgets = [{"end_date": "2020-07-08", "amount": 100},
                    {"end_date": "2099-01-01", "amount": 200}]

        self.assertRaises(IncorrectDateFormatException, calculate_weekly_budget, self.week_start, self.week_end, self.budgets)

    def test_no_budgets(self):
        ''' Test that the correct exception is raised when no budgets are passed '''
        self.budgets = []

        self.assertRaises(NoBudgetException, calculate_weekly_budget, self.week_start, self.week_end, self.budgets)

    def test_incorrect_budget_object(self):
        ''' Test that the correct exception is raised when an incorrect budget object is passed '''
        self.budgets = [{"start_date": "2020-07-08", "value": 100}]

        self.assertRaises(IncorrectBudgetFormatException, calculate_weekly_budget, self.week_start, self.week_end, self.budgets)

class GetRecentWeeklyTestCase(unittest.TestCase):
    ''' Tests for the get_recent_weekly method '''
    # todo
    pass

class GetWeeklyExpenditureTestCase(unittest.TestCase):
    ''' Tests for the get_weekly_expenditure method '''
    # todo
    pass