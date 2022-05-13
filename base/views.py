import io
import mimetypes

import requests
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework.views import APIView

from base.models import Expenses
from expenseTracker.settings import SENDER, SECRET_SAUCE
from django.core.mail import EmailMessage


class ExpensesPDF(APIView):
    @staticmethod
    def send_pdf(user):
        username = user.username.split("@")[0]
        email = EmailMessage(
            "Tu resumen mensual",
            f"Hola {username}! En este correo vas a encontrar tu resumen de gastos del mes.\n\n"
            f"Que tengas un buen día!",
            SENDER,
            [user.username],
        )
        email.attach_file("Reporte Mensual.pdf")
        email.send()

    @staticmethod
    def build_pdf(expenses):
        buf = io.BytesIO()

        p = canvas.Canvas("Reporte Mensual.pdf", pagesize=letter, bottomup=0)
        p.setTitle("Reporte Mensual")
        text_object = p.beginText()
        text_object.setTextOrigin(inch, inch)
        text_object.setFont("Helvetica", 14)

        exps = list()
        expenses_by_currency = {
            "USD": 0,
            "EUR": 0,
            "BTC": 0,
            "CHF": 0,
            "GBP": 0,
            "ARS": 0,
        }

        for expense in expenses:
            expenses_by_currency[str(expense.final_currency)] += float(
                expense.final_amount
            )
            exps.append(
                f"{str(expense.title):<25}{str(expense.created.date()):<25}"
                f"{str(expense.final_amount)} {str(expense.final_currency)}"
            )

        text_object.textLine(f"{'':<45}{'Reporte Mensual'}")
        text_object.textLine("")
        text_object.textLine(f"{'Descripción':<35}{'Fecha':<25}{'Valor'}")
        text_object.textLine("")

        [text_object.textLine(exp) for exp in exps]

        text_object.textLine("")
        text_object.textLine("")
        text_object.textLine(f"{'':<45}{'Gastos totales del mes'}")
        text_object.textLine("")
        for currency, total in expenses_by_currency.items():
            text_object.textLine(f"{currency}: {total}")

        p.drawText(text_object)

        p.save()

        buf.seek(0)

    def post(self, request):
        data = request.data
        if data.get("secret_sauce") == SECRET_SAUCE:
            users = get_user_model().objects.all()
            user_expenses = list()
            for user in users:
                exp = Expenses.objects.filter(user=user)
                if exp:
                    self.build_pdf(exp)
                    self.send_pdf(user)

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

    @staticmethod
    def calculate_current_total(expenses):
        current_total = dict()
        for expense in expenses:
            current_total[expense.final_currency] += expense.final_amount

        current_total = {k: v for k, v in current_total.items() if v != 0}

        return current_total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expenses"] = context["expenses"].filter(user=self.request.user)
        context["current_total"] = self.calculate_current_total(context["expenses"])

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


class PdfButton(LoginRequiredMixin, View):
    @staticmethod
    def build_pdf(expenses):
        buf = io.BytesIO()

        p = canvas.Canvas("Reporte Mensual.pdf", pagesize=letter, bottomup=0)
        p.setTitle("Reporte Mensual")
        text_object = p.beginText()
        text_object.setTextOrigin(inch, inch)
        text_object.setFont("Helvetica", 14)

        exps = list()
        expenses_by_currency = {
            "USD": 0,
            "EUR": 0,
            "BTC": 0,
            "CHF": 0,
            "GBP": 0,
            "ARS": 0,
        }

        for expense in expenses:
            expenses_by_currency[str(expense.final_currency)] += float(
                expense.final_amount
            )
            exps.append(
                f"{str(expense.title):<25}{str(expense.created.date()):<25}"
                f"{str(expense.final_amount)} {str(expense.final_currency)}"
            )

        text_object.textLine(f"{'':<45}{'Reporte Mensual'}")
        text_object.textLine("")
        text_object.textLine(f"{'Descripción':<35}{'Fecha':<25}{'Valor'}")
        text_object.textLine("")

        [text_object.textLine(exp) for exp in exps]

        text_object.textLine("")
        text_object.textLine("")
        text_object.textLine(f"{'':<45}{'Gastos totales del mes'}")
        text_object.textLine("")
        for currency, total in expenses_by_currency.items():
            text_object.textLine(f"{currency}: {total}")

        p.drawText(text_object)

        p.save()

        buf.seek(0)

    def get(self, request):
        users = get_user_model().objects.all()

        for user in users:
            exp = Expenses.objects.filter(user=user)
            if exp:
                self.build_pdf(exp)
        path = open("Reporte Mensual.pdf", "rb")
        # Set the mime type
        mime_type, _ = mimetypes.guess_type("Reporte Mensual.pdf")
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response["Content-Disposition"] = (
            "attachment; filename=%s" % "Reporte Mensual.pdf"
        )
        # Return the response value
        return response
