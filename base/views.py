from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.
from base.models import Expenses


class ExpenseList(ListView):
    model = Expenses
    context_object_name = "expenses"


class ExpenseDetail(DetailView):
    model = Expenses
    context_object_name = "expense"
    template_name = "base/expense.html"
