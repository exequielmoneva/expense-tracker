from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from base.models import Expenses


class ExpenseList(ListView):
    model = Expenses
    context_object_name = "expenses"


class ExpenseDetail(DetailView):
    model = Expenses
    context_object_name = "expense"
    template_name = "base/expense.html"


class ExpenseCreate(CreateView):
    model = Expenses
    # fields = ['title', 'description', 'total_amount', 'original_currency', 'final_currency']
    fields = "__all__"
    success_url = reverse_lazy("expenses")


class ExpenseUpdate(UpdateView):
    model = Expenses
    fields = "__all__"
    success_url = reverse_lazy("expenses")


class ExpenseDelete(DeleteView):
    model = Expenses
    context_object_name = "expense"
    success_url = reverse_lazy("expenses")
