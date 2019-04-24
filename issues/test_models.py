from django.test import TestCase
from django.contrib.auth.models import User

from issues.models import Issue, Upvote, Comment

class TestIssuesModels(TestCase):
    def setUp(self):
        User.objects.create(username="test_user", password="test_password")
        test_user = User.objects.get(username="test_user")
        Issue.objects.create(title="test_issue", author=test_user, description="test", issue_type="BG")
        test_issue = Issue.objects.get(title="test_issue")
        Upvote.objects.create(author=test_user, related_issue=test_issue)
        Comment.objects.create(author=test_user, related_issue=test_issue, content="test")
        
    def test_issue_str_method(self):
        test_issue = Issue.objects.get(title="test_issue")
        self.assertEqual("test_issue", str(test_issue))
        
    def test_can_get_issue_long_status(self):
        test_issue = Issue.objects.get(title="test_issue")
        self.assertEqual("IC", test_issue.status)
        self.assertEqual("Incomplete", test_issue.status_long)
        
    def test_upvote_str_method(self):
        test_user = User.objects.get(username="test_user")
        test_issue = Issue.objects.get(title="test_issue")
        test_upvote = Upvote.objects.get(author=test_user)
        self.assertEqual('Upvote on %s by %s' % (test_issue.title, test_user.username), str(test_upvote))
        
    def test_comment_str_method(self):
        test_user = User.objects.get(username="test_user")
        test_issue = Issue.objects.get(title="test_issue")
        test_comment = Comment.objects.get(author=test_user)
        self.assertEqual('Comment on %s by %s' % (test_issue.title, test_user.username), str(test_comment))
        
    
        
    