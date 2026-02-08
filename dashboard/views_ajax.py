from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from linkif.models import Vaga, Candidatura
from linkif.forms import VagaForm
import time
from django.contrib.messages import get_messages

@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
def ajax_vaga_detalhe(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    html = render_to_string(
        "dashboard/partials/_vaga_detalhe.html",
        {"vaga": vaga},
        request=request
    )
    return JsonResponse({"html": html})

@login_required
@permission_required("usuarios.can_post_vaga", raise_exception=True)
def ajax_vaga_form(request, vaga_id=None):
    """
    GET  -> retorna formulário (criar ou editar)
    POST -> salva vaga
    """
    vaga = None

    if vaga_id:
        vaga = get_object_or_404(Vaga, id=vaga_id)

        # empresa só edita a própria vaga
        if request.user.tipo == "empresa" and vaga.empresa != request.user:
            return HttpResponseForbidden()

    if request.method == "POST":
        form = VagaForm(request.POST, instance=vaga)

        if form.is_valid():
            vaga = form.save(commit=False)

            if not vaga_id:
                vaga.empresa = request.user
                vaga.status = "pendente"
            else:
                vaga.status = "pendente"

            vaga.save()

            return JsonResponse({"success": True})

        html = render_to_string(
            "dashboard/partials/_vaga_form.html",
            {"form": form, "vaga": vaga},
            request=request
        )
        return JsonResponse({"success": False, "html": html})

    else:
        form = VagaForm(instance=vaga)

        html = render_to_string(
            "dashboard/partials/_vaga_form.html",
            {"form": form, "vaga": vaga},
            request=request
        )

        return JsonResponse({"html": html})

@login_required
@permission_required("usuarios.acesso_empresa", raise_exception=True)
def ajax_vaga_excluir(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.user.tipo == "empresa" and vaga.empresa != request.user:
        return JsonResponse({"erro": "Sem permissão"}, status=403)

    if request.method == "POST":
        Candidatura.objects.filter(vaga=vaga).delete()
        vaga.delete()
        return JsonResponse({"success": True})

    html = render_to_string(
        "dashboard/partials/_vaga_excluir.html",
        {
            "vaga": vaga,
            "action_url": request.path
        },
        request=request
    )
    return JsonResponse({"html": html})

from django.http import JsonResponse

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def ajax_aprovar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.method == "POST":
        vaga.status = "aprovada"
        vaga.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})

@login_required
@permission_required("usuarios.acesso_coordenacao", raise_exception=True)
def ajax_reprovar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if request.method == "POST":
        vaga.status = "reprovada"
        vaga.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})

def ajax_mensagens(request):
    messages = get_messages(request)
    return render(request, 'partials/_messages.html', {'messages': messages})