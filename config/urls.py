from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("linkif.urls")),              # site principal
   # path("dashboard/", include("dashboard.urls")),  # painéis internos
    path("usuarios/", include("usuarios.urls")),    # autenticação e perfis
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout padrão
    path("admin/", admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
