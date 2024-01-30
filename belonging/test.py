import unittest

from django.test import TestCase
from django.urls import reverse

from .views import RegistrationView


class RegistrationViewTestCase(TestCase):

    def test_get(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/registration.html')

    def test_post(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '1-800-555-1212',
            'password': 'password',
            'confirm_password': 'password',
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_invalid_data(self):
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'password': '',
            'confirm_password': '',
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/registration.html')
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'phone_number', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'confirm_password', 'This field is required.')