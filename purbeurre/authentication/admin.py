from django.contrib import admin

# Register your models here.

from .models import User
from products.models import Substitute


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    fields = ('email', 'first_name', 'last_name')
    readonly_fields = ['email']
    list_display = (
        'email',
        'first_name',
        'last_name',
        'last_login',
        'qte_substitute'
        )

    def qte_substitute(self, db_field):
        substitute_sum = Substitute.objects.filter(user_id=db_field.id).count()
        return substitute_sum
    qte_substitute.short_description = "Quantité de Substitus sauvés"
