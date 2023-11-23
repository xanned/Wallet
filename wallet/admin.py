from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from wallet.models import Wallet, Transaction


class TransactionInstanceInline(admin.TabularInline):
    model = Transaction
    fk_name = "wallet"
    extra = 0


class TransferInstanceInline(admin.TabularInline):
    model = Transaction
    fk_name = "transfer_wallet"
    extra = 0


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "currency", "amount")
    inlines = [TransactionInstanceInline, TransferInstanceInline]
    fieldsets = (
        ("Wallet", {
            'fields': ('user_id', 'currency', 'amount')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("datetime", "wallet", "action", "amount")


class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0
    show_change_link = True
    can_delete = False
    verbose_name_plural = 'Wallets'


class UserAdmin(BaseUserAdmin):
    inlines = [WalletInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
