from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # site público
    path("", include("linkif.urls")),              
    
    # dashboard privado
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    
    # login / cadastro / recuperação de senha personalizados
    path("usuarios/", include("usuarios.urls")),
    
    # painel admin
    path("admin/", admin.site.urls),
    path("vagas/", include(("linkif.urls", "vagas"), namespace="vagas")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
