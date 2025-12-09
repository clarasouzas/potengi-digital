from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # site público
    path("", include("linkif.urls")),              
    
    # dashboard privado
    path("dashboard/", include("dashboard.urls")),
    
    # login / cadastro / recuperação de senha personalizados
    path("usuarios/", include("usuarios.urls")),
    
    # painel admin
    path("admin/", admin.site.urls),
    
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
