from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

"""class Expense(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_owner')

    def __str__(self):
        return self.name


"""


class Expenses(models.Model):
    CURRENCY_CHOICES = (
        ("usd", "USD"),
        ("eur", "EUR"),
        ("btc", "BTC"),
        ("chf", "CHF"),
        ("gbp", "GBP"),
        ("ars", "ARS"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    original_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default="eur"
    )
    final_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default="eur"
    )
    total_amount = models.FloatField(default=0.01, validators=[MinValueValidator(0.01)])

    def __srt__(self):
        return self.title

    class Meta:
        # order_with_respect_to = 'user'
        ordering = ["-created"]
