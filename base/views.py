import requests
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from reportlab.pdfgen import canvas
from rest_framework.views import APIView

from base.models import Expenses
from expenseTracker.settings import SENDER, SECRET_SAUCE


class ExpensesPDF(APIView):
    @staticmethod
    def build_pdf(expenses):

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas("Reporte Mensual.pdf")

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        for expense in expenses:
            p.drawString(
                expense.title,
                expense.created,
                f"{expense.final_amount} {expense.final_currency}",
            )

        # Close the PDF object cleanly, and we're done.
        # p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        return FileResponse(p, as_attachment=True, filename="hello.pdf")

    def post(self, request):
        data = request.data
        if data.get("secret_sauce") == SECRET_SAUCE:
            users = get_user_model().objects.all()
            user_expenses = list()
            for user in users:
                """for expense in Expenses.objects.filter(user=user):
                user_expenses.append(expense.title)"""
                return HttpResponse(
                    self.build_pdf(Expenses.objects.filter(user=user)), 200
                )

            return HttpResponse(user_expenses, 200)


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
            username = user.username.split("@")[0]
            send_mail(
                "Bienvenido a Gasto Control!",
                f"Hola {username}! En este correo vas a encontrar tus credenciales para que no las pierdas:\n\n"
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
    @staticmethod
    def __exchange_currency(user):
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
