from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class SignUpTests(TestCase):
	def test_signup_creates_user_and_profile(self):
		client = Client()
		url = reverse('App:signup')
		data = {
			'username': 'testuser',
			'full_name': 'Test User',
			'email': 'testuser@example.com',
			'phone': '1234567890',
			'work_status': 'findjob',
			'password1': 'testpassword123',
			'password2': 'testpassword123',
		}
		response = client.post(url, data, follow=True)
		# Should return HTTP 200 and no form errors
		self.assertEqual(response.status_code, 200)
		form = response.context.get('form')
		if form and form.errors:
			self.fail(f"Form errors: {form.errors}")
		# User should exist
		user = User.objects.filter(email='testuser@example.com').first()
		self.assertIsNotNone(user)
		# Profile should exist and contain phone
		profile = Profile.objects.filter(user=user).first()
		self.assertIsNotNone(profile)
		self.assertEqual(profile.phone, '1234567890')

		# After signup user is logged in and redirected to their profile
		redirect_chain = response.redirect_chain
		self.assertTrue(any(f"/candidate-profile/{user.username}/" in location for location, code in redirect_chain), f"Redirect chain: {redirect_chain}")


class LoginTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.username = 'loginuser'
		self.email = 'loginuser@example.com'
		self.password = 'testpassword123'
		self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

	def test_login_with_correct_credentials(self):
		url = reverse('App:login')
		data = {
			'username': self.username,
			'password': self.password,
		}
		response = self.client.post(url, data, follow=True)
		self.assertEqual(response.status_code, 200)
		# After login, user should be authenticated in session
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)
		# Should redirect to candidate profile detail for this username
		redirect_chain = response.redirect_chain
		self.assertTrue(any(f"/candidate-profile/{self.username}/" in location for location, code in redirect_chain), f"Redirect chain: {redirect_chain}")

	def test_failed_login_reopens_modal_and_shows_message(self):
		url = reverse('App:login')
		next_url = reverse('App:index')
		data = {'username': 'wronguser', 'password': 'notvalid', 'next': next_url}
		response = self.client.post(url, data, follow=True)
		self.assertEqual(response.status_code, 200)
		# Ensure not authenticated
		user = response.context.get('user')
		self.assertFalse(user.is_authenticated)
		# Redirect chain should include ?login=failed
		redirect_chain = response.redirect_chain
		self.assertTrue(any('login=failed' in location for location, code in redirect_chain), f"Redirect chain: {redirect_chain}")
		# Messages should contain error text
		messages_list = list(response.context.get('messages'))
		self.assertTrue(any('Invalid username or password' in str(m) for m in messages_list), f"Messages: {messages_list}")

	def test_logout_logs_out_user(self):
		# login via client
		login = self.client.login(username=self.username, password=self.password)
		self.assertTrue(login)
		response = self.client.get(reverse('App:logout'), follow=True)
		self.assertEqual(response.status_code, 200)
		user = response.context.get('user')
		self.assertFalse(user.is_authenticated)
		# Should show logout message
		messages_list = list(response.context.get('messages'))
		self.assertTrue(any('logged out' in str(m) for m in messages_list))
