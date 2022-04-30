import random

from django.contrib.auth.views import LogoutView
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from base.views import (
    CustomLoginView,
    RegisterPage,
    ExpenseCreate,
    ExpenseDetail,
    ExpenseUpdate,
    ExpenseDelete,
)


class TestUrls(SimpleTestCase):
    def test_login_url_resolved(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_url_resolved(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func.view_class, RegisterPage)

    def test_expense_detail_url_resolved(self):
        url = reverse("expense", args=[random.randint(0, 9)])
        self.assertEquals(resolve(url).func.view_class, ExpenseDetail)

    def test_expense_update_url_resolved(self):
        url = reverse("expense-update", args=[random.randint(0, 9)])
        self.assertEquals(resolve(url).func.view_class, ExpenseUpdate)

    def test_expense_delete_url_resolved(self):
        url = reverse("expense-delete", args=[random.randint(0, 9)])
        self.assertEquals(resolve(url).func.view_class, ExpenseDelete)

    def test_expense_create_url_resolved(self):
        url = reverse("expense-create")
        self.assertEquals(resolve(url).func.view_class, ExpenseCreate)
