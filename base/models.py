from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Expenses(models.Model):
    CURRENCY_CHOICES = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BTC", "BTC"),
        ("CHF", "CHF"),
        ("GBP", "GBP"),
        ("ARS", "ARS"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    original_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default="EUR"
    )
    final_currency = models.CharField(
        max_length=10, choices=CURRENCY_CHOICES, default="EUR"
    )
    original_amount = models.FloatField(
        default=0.01, validators=[MinValueValidator(0.01)]
    )
    final_amount = models.FloatField(default=0.01)

    def __srt__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
