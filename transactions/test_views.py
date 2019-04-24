from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestTransactionsViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password")
        
    def test_get_begin_purchase_page(self):
        self.client.login(username='test_user', password='test_password')
        
        response = self.client.get(reverse("begin_purchase"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "begin_purchase.html")
        
    def test_begin_purchase_redirects_to_continue_purchase_and_stores_upvotes_amount_in_session(self):
        self.client.login(username='test_user', password='test_password')
        data = {
            "upvotes_amount": "20"
        }
        response = self.client.post(reverse("begin_purchase"), data)
        
        session = self.client.session
        amount = session['purchase']
        
        self.assertEqual(20, amount)
        self.assertRedirects(response, reverse("continue_purchase"), status_code=302)
        
    def test_get_continue_purchase_page(self):
        self.client.login(username='test_user', password='test_password')
        
        session = self.client.session
        session['purchase'] = "20"
        session.save()
        
        response = self.client.get(reverse("continue_purchase"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "continue_purchase.html")
        
    def test_get_finish_purchase_page(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username="test_user")
        user.profile.upvotes_owned += 10
        user.profile.save()
        
        response = self.client.get(reverse("finish_purchase"))
        
        amount_owned = response.context["upvotes_owned"]
        self.assertEqual(user.profile.upvotes_owned, amount_owned)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "finish_purchase.html")