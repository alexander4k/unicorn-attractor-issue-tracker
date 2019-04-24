from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Profile
from .models import Issue, Comment, Upvote

class TestIssuesViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        
    def test_get_all_issues_page(self):
        response = self.client.get(reverse("all_issues"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_issues.html")
        
    def test_get_bugs_page(self):
        response = self.client.get(reverse("bugs"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bugs.html")
        
    def test_get_features_page(self):
        response = self.client.get(reverse("features"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "features.html")
        
    def test_get_create_issue_page_when_no_profile(self):
        user = User.objects.get(username="test_user")
        Profile.objects.filter(user=user).delete()
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("create_issue"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        
    def test_get_create_issue_page_if_logged_in(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse("create_issue"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_issue.html")
  
    def test_if_create_issue_page_refreshes_when_form_invalid(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        
        post_data = {
            "title": "test",
            "author": user,
            "description": "description",
            "issue": "BG"
        }
        
        response = self.client.post(reverse("create_issue"), post_data, follow=True)
        self.assertRedirects(response, reverse("create_issue"), status_code=302)
        self.assertTemplateUsed(response, "create_issue.html")
        
    def test_if_create_issue_redirects_to_issue_details_when_form_valid(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        
        post_data = {
            "title": "test",
            "author": user,
            "description": "description",
            "issue_type": "BG"
        }
        
        response = self.client.post(reverse("create_issue"), post_data, follow=True)
        issue = Issue.objects.get(title="test")
        self.assertRedirects(response, "/issues/issue_details1/", status_code=302)
        self.assertTemplateUsed(response, "issue_details.html")
        
    def test_if_delete_issues_redirects_to_404_if_no_issue(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get("/issues/delete_issue2/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        
    def test_if_delete_issue_deletes_given_issue_and_redirects_to_all_issues(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Issue.objects.create(title="test", author=user, issue_type="BG", description="test")
        response = self.client.get("/issues/delete_issue1/")
        self.assertRedirects(response, reverse("all_issues"), status_code=302)
        
    def test_if_issue_details_page_displays_404_page_when_form_invalid(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Issue.objects.create(title="test", author=user, issue_type="BG", description="test")
        issue = Issue.objects.get(title="test")
        
        post_data = {
            "author": user,
            "related": issue,
            "co": "test"
        }
        
        response = self.client.post("/issues/issue_details1/", post_data, follow=True)
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "500.html")
        
    def test_if_issue_details_creates_a_comment_when_form_valid_and_refreshes(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Issue.objects.create(title="test", author=user, issue_type="BG", description="test")
        issue = Issue.objects.get(title="test")
        
        post_data = {
            "author": user,
            "related_issue": issue,
            "content": "test"
        }
        
        response = self.client.post("/issues/issue_details1/", post_data, follow=True)
        comment = Comment.objects.get(author=user)
        self.assertEqual("test", comment.content)
        self.assertRedirects(response, "/issues/issue_details1/", status_code=302)
        self.assertTemplateUsed(response, "issue_details.html")
        
    def test_if_upvote_issue_redirects_to_403_if_no_profile(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Profile.objects.filter(user=user).delete()
        response = self.client.get("/issues/add_upvote1/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        
    def test_if_add_upvote_redirects_to_404_if_no_issue(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get("/issues/delete_issue2/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")    
        
    def test_get_can_add_upvote_and_redirect_to_issue_details(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Issue.objects.create(title="test", author=user, issue_type="BG", description="test")
        issue = Issue.objects.get(title="test")
        
        response = self.client.get("/issues/add_upvote1/")
        self.assertRedirects(response, "/issues/issue_details1/", status_code=302)
        
    def test_get_can_add_upvote_even_if_already_upvoted_feature(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        user.profile.upvotes_owned += 10
        user.profile.save()
        Issue.objects.create(title="test", author=user, issue_type="FR", description="test")
        issue = Issue.objects.get(title="test")
        Upvote.objects.create(author=user, related_issue=issue)
        
        response = self.client.get("/issues/add_upvote1/")
        self.assertRedirects(response, "/issues/issue_details1/", status_code=302)
        
    def test_if_add_upvote_redirects_to_issue_details_if_issue_type_not_fr_or_br(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        Issue.objects.create(title="test", author=user, issue_type="none", description="test")
        
        response = self.client.get("/issues/add_upvote1/")
        self.assertRedirects(response, "/issues/issue_details1/", status_code=302)