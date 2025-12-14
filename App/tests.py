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


class RoleAssignTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.rpo = User.objects.create_user(username='rpo_test', password='RpoPass123')
		Profile.objects.create(user=self.rpo, role='rpo_admin')

		self.cand = User.objects.create_user(username='cand_test', password='CandPass123')
		Profile.objects.create(user=self.cand, role='candidate')

	def test_rpo_can_access_assign_roles(self):
		self.client.login(username='rpo_test', password='RpoPass123')
		url = reverse('App:assign_roles')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		# Should show page header
		self.assertContains(response, 'Assign Roles')

	def test_non_rpo_forbidden(self):
		self.client.login(username='cand_test', password='CandPass123')
		url = reverse('App:assign_roles')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)

	def test_rpo_can_change_role(self):
		self.client.login(username='rpo_test', password='RpoPass123')
		url = reverse('App:assign_roles')
		data = {'username': 'cand_test', 'role': 'hiring_manager'}
		response = self.client.post(url, data, follow=True)
		self.assertEqual(response.status_code, 200)
		profile = Profile.objects.get(user__username='cand_test')
		self.assertEqual(profile.role, 'hiring_manager')

	def test_navbar_shows_link_for_rpo(self):
		self.client.login(username='rpo_test', password='RpoPass123')
		response = self.client.get(reverse('App:index'))
		self.assertContains(response, 'Assign Roles')

	def test_navbar_hides_link_for_candidate(self):
		self.client.login(username='cand_test', password='CandPass123')
		response = self.client.get(reverse('App:index'))
		self.assertNotContains(response, 'Assign Roles')

	def test_ajax_role_change(self):
		self.client.login(username='rpo_test', password='RpoPass123')
		url = reverse('App:assign_role_ajax')
		data = {'username': 'cand_test', 'role': 'hiring_manager'}
		response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.json().get('ok'))
		profile = Profile.objects.get(user__username='cand_test')
		self.assertEqual(profile.role, 'hiring_manager')

	def test_ajax_forbidden_for_non_rpo(self):
		self.client.login(username='cand_test', password='CandPass123')
		url = reverse('App:assign_role_ajax')
		data = {'username': 'rpo_test', 'role': 'candidate'}
		response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 403)
