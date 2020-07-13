from django.test import TestCase
from ..templatetags.form_tags import input_class,field_type
from django import forms


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['name', 'password']


class FieldTypeTests(TestCase):
    def test_form_field_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))


class InputClassTests(TestCase):
    def test_unbound_field(self):
        form = ExampleForm()
        self.assertEquals('form-control ', input_class(form['name']))

    def test_valid_input_field(self):
        form = ExampleForm({'name':'john','password':'123'})
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))

    def test_invalid_input_field(self):
        form = ExampleForm({'name':'', 'password':'123'})
        self.assertEquals('form-control is-invalid',input_class(form['name']))
        self.assertEquals('form-control ',input_class(form['password']))