from django.urls import path
from .views import (
    ExpenseList,
    ExpenseDetail,
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseDelete,
)

urlpatterns = [
    path("", ExpenseList.as_view(), name="expenses"),
    path("expense/<int:pk>", ExpenseDetail.as_view(), name="expense"),
    path("expense-create/", ExpenseCreate.as_view(), name="expense-create"),
    path("expense-update/<int:pk>", ExpenseUpdate.as_view(), name="expense-update"),
    path("expense-delete/<int:pk>", ExpenseDelete.as_view(), name="expense-delete"),
]
