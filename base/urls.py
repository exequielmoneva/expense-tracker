from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    ExpenseList,
    ExpenseDetail,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseDelete,
    CustomLoginView,
    RegisterPage,
    PdfButton,
    ExpensesPDF,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("", ExpenseList.as_view(), name="expenses"),
    path("expense/<int:pk>", ExpenseDetail.as_view(), name="expense"),
    path("expense-create/", ExpenseCreate.as_view(), name="expense-create"),
    path("expense-update/<int:pk>", ExpenseUpdate.as_view(), name="expense-update"),
    path("expense-delete/<int:pk>", ExpenseDelete.as_view(), name="expense-delete"),
    path("expense-pdf", PdfButton.as_view(), name="expense-pdf"),
    path("monthly-pdf-resume", ExpensesPDF.as_view(), name="monthly-pdf-resume"),
]
