from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from e_wallet import settings
from wallet.views import WalletDeposit, WalletWithdrawal, WallerTransfer

router = SimpleRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('deposit', WalletDeposit.as_view()),
    path('withdrawal', WalletWithdrawal.as_view()),
    path('transfer', WallerTransfer.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
