import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from base.models import Expenses
from expenseTracker.settings import SENDER


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("expenses")


class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("expenses")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            send_mail(
                "Bienvenido a Gasto Control!",
                f"Hola {user.username}! En este correo vas a encontrar tus credenciales para que no las pierdas:\n\n"
                f"Usuario: {user.username}\n"
                f'Contraseña: {form.cleaned_data["password1"]}\n\n'
                f"Que tengas un buen día!",
                SENDER,
                [user.username],
                fail_silently=False,
            )
            login(self.request, user)

        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("expenses")
        return super(RegisterPage, self).get(*args, **kwargs)


class ExpenseList(LoginRequiredMixin, ListView):
    model = Expenses
    context_object_name = "expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expenses"] = context["expenses"].filter(user=self.request.user)

        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["expenses"] = context["expenses"].filter(
                title__icontains=search_input
            )

        context["search_input"] = search_input

        return context


class ExpenseDetail(LoginRequiredMixin, DetailView):
    model = Expenses
    context_object_name = "expense"
    template_name = "base/expense.html"


class ExpenseCreate(LoginRequiredMixin, CreateView):
    def __exchange_currency(self, user):
        url = (
            f"https://api.exchangerate.host/convert?from={user.original_currency}&"
            f"to={user.final_currency}&{user.original_amount}=10"
        )
        response = requests.get(url)
        data = response.json()
        return round(data.get("result"), 2)

    model = Expenses
    fields = [
        "title",
        "description",
        "original_amount",
        "original_currency",
        "final_currency",
    ]
    success_url = reverse_lazy("expenses")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.final_amount = self.__exchange_currency(form.instance)
        return super(ExpenseCreate, self).form_valid(form)


class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = [
        "title",
        "description",
        "original_amount",
        "original_currency",
        "final_currency",
    ]
    success_url = reverse_lazy("expenses")


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expenses
    context_object_name = "expense"
    success_url = reverse_lazy("expenses")


class ExpenseReorder(View):
    def post(self, request):
        return redirect(reverse_lazy("expenses"))
