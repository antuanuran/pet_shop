from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from apps.orders.models import Order, OrderRow


class OrderRowInLineFormset(BaseInlineFormSet):
    def clean(self):
        count_all = 0
        for form in self.forms:
            if form.cleaned_data["DELETE"]:
                continue
            if form.cleaned_data["qty"] > form.cleaned_data["item"].count:
                raise ValidationError(
                    f"Max Limit count  [{form.cleaned_data['item'].catalog.name}] - {form.cleaned_data['item'].count}"
                )
            else:
                count_all += form.cleaned_data["qty"]
                if count_all > form.cleaned_data["item"].count:
                    raise ValidationError(
                        f"Превыш. лимит  [{form.cleaned_data['item'].catalog.name}] - {form.cleaned_data['item'].count}"
                    )
        super().clean()


class OrderRowInLine(admin.TabularInline):
    model = OrderRow
    extra = 0
    readonly_fields = ["sum_current_order"]
    formset = OrderRowInLineFormset

    # Добавление поля для поисковой строки в Админке


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["number_order", "user", "status", "created_at", "updated_at", "sum_total_all_orders", "id"]
    readonly_fields = ["sum_total_all_orders"]
    ordering = ["-created_at"]
    inlines = [OrderRowInLine]
