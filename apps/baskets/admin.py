from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from apps.baskets.models import Basket, BasketRow


class BasketRowInLineFormset(BaseInlineFormSet):
    def clean(self):
        count_all = 0
        for form in self.forms:
            if form.cleaned_data["DELETE"]:
                continue
            if form.cleaned_data["qty"] > form.cleaned_data["item"].count:
                raise ValidationError(
                    f"Превышено кол-во  [{form.cleaned_data['item'].catalog.name}] - {form.cleaned_data['item'].count}"
                )
            else:
                count_all += form.cleaned_data["qty"]
                if count_all > form.cleaned_data["item"].count:
                    raise ValidationError(
                        f"Превыш. лимит  [{form.cleaned_data['item'].catalog.name}] - {form.cleaned_data['item'].count}"
                    )
        super().clean()


class BasketRowInLine(admin.TabularInline):
    model = BasketRow
    extra = 0
    readonly_fields = ["price_unit", "summa_price", "is_active_item"]
    formset = BasketRowInLineFormset

    @admin.display(boolean=True)
    def is_active_item(self, obj):
        if obj.item.is_active:
            return True
        else:
            return False


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["number_baskets", "user", "total_price_all_basket"]
    readonly_fields = ["total_price_all_basket"]
    inlines = [BasketRowInLine]
    search_fields = ["user__email"]
