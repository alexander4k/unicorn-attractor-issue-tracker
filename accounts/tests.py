from django.test import TestCase
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

from issues.models import Issue
from .utils import misc

class TestAccounts(TestCase):
    """
    Tests for accounts
    """
    def setUp(self):
        User.objects.create(username="test_user", password="test_password")
        test_user = User.objects.get(username="test_user")
        Issue.objects.create(title="test_issue", author=test_user, description="test", issue_type="BG")
        issue = Issue.objects.get(title="test_issue")
        issue.completed = timezone.now() + relativedelta(days=-3)
        issue.save()
        
    def test_can_get_date_for_today(self):
        today = timezone.now()
        returned_date = misc.get_previous_dates("0", "0", 2)[0]
        self.assertEqual(today.year, returned_date.year)
        self.assertEqual(today.month, returned_date.month)
        self.assertEqual(today.day, returned_date.day)
        
    def test_can_get_list_of_seven_days_backwards_from_20_days_ago(self):
        seven_previous_days = []
        
        for i in range(1, 8):
            seven_previous_days.append(timezone.now() + relativedelta(days=-i-20))

        seven_previous_days_test = misc.get_previous_dates("0", "-i-20", 8)

        for index, day in enumerate(seven_previous_days):
            self.assertEqual(day.day, seven_previous_days_test[index].day)
            
    def test_can_get_list_of_issue_counts_for_last_seven_days(self):
        seven_previous_days = []
        issue_counts = []
        
        for i in range(1, 8):
            seven_previous_days.append(timezone.now() + relativedelta(days=-i))
            
        for date in seven_previous_days:
            issue_counts.append(Issue.objects.filter(completed__month=date.month, completed__year=date.year, completed__day=date.day).count())

        issue_counts_test = misc.get_issues_per_timerange(seven_previous_days)

        self.assertEqual(issue_counts, issue_counts_test)
        
    def test_can_get_list_of_issue_counts_for_last_twelve_months(self):
        issue = Issue.objects.get(title="test_issue")
        issue.completed = timezone.now() + relativedelta(months=-3)
        issue.save()
        
        twelve_previous_months = []
        issue_counts = []
        
        for i in range(1, 13):
            twelve_previous_months.append(timezone.now() + relativedelta(months=-i))

        for date in twelve_previous_months:
            issue_counts.append(Issue.objects.filter(completed__month=date.month, completed__year=date.year).count())
        
        issue_counts_test = misc.get_issues_per_timerange(twelve_previous_months)

        self.assertEqual(issue_counts, issue_counts_test)
        
    def test_can_get_count_of_issues_by_status(self):
        test_user = User.objects.get(username="test_user")
        Issue.objects.create(title="test_issue2", author=test_user, description="test", issue_type="BG", status="IC")
        Issue.objects.create(title="test_issue3", author=test_user, description="test", issue_type="BG", status="IP")
        Issue.objects.create(title="test_issue4", author=test_user, description="test", issue_type="BG", status="IC")
        Issue.objects.create(title="test_issue5", author=test_user, description="test", issue_type="BG", status="CT")
        
        list_of_counts = misc.get_count_of_issues_by_status()
        
        self.assertEqual([1, 1, 3], list_of_counts)
        