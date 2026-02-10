from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from linkif.models import Vaga
from linkif.forms import VagaForm


# ===================== LISTAR =====================
@login_required
def ajax_listar_vagas(request):

    if request.user.tipo == "empresa":
        vagas = Vaga.objects.filter(empresa=request.user)
    elif request.user.tipo == "coordenador":
        vagas = Vaga.objects.all()
    else:
        vagas = Vaga.objects.none()

    vagas = vagas.order_by("-id")

    context = {
        "objects": vagas,
        "url_detalhar": "dashboard:ajax_detalhar_vaga",
        "url_editar": "dashboard:ajax_editar_vaga",
        "url_remover": "dashboard:ajax_remover_vaga",
    }

    return render(
        request,
        "dashboard/partials/vagas/_lista_vagas_cards.html",
        context
    )


# ===================== CRIAR =====================
@login_required
def ajax_criar_vaga(request):

    if request.method == "POST":
        form = VagaForm(request.POST)

        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user

            if request.user.tipo == "coordenador":
                vaga.status = "aprovada"
                vaga.etapa = "publicada"
                vaga.data_publicacao = timezone.now()
                vaga.aprovado_por = request.user
                messages.success(
                    request,
                    "Vaga criada e publicada com sucesso."
                )
            else:
                vaga.status = "pendente"
                vaga.etapa = "pendente_aprovacao"
                messages.info(
                    request,
                    "Vaga criada e enviada para aprovação."
                )

            vaga.save()
            return JsonResponse({"ok": True}, status=201)

        # formulário inválido → devolve HTML do form
        return render(
            request,
            "dashboard/partials/vagas/_vaga_form.html",
            {
                "form": form,
                "nome": "vaga",
                "erro": "Erro ao criar vaga. Verifique os dados.",
            },
            status=400
        )

    return render(
        request,
        "dashboard/partials/vagas/_vaga_form.html",
        {
            "form": VagaForm(),
            "nome": "vaga",
        }
    )


# ===================== EDITAR =====================
@login_required
def ajax_editar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)

    if request.user.tipo == "empresa" and vaga.empresa != request.user:
        return JsonResponse({"ok": False}, status=403)

    if request.method == "POST":
        form = VagaForm(request.POST, instance=vaga)

        if form.is_valid():
            vaga = form.save(commit=False)

            if request.user.tipo == "empresa":
                vaga.status = "pendente"
                vaga.etapa = "pendente_aprovacao"
                vaga.aprovado_por = None
                vaga.data_publicacao = None
                messages.info(
                    request,
                    "Alterações enviadas para nova aprovação."
                )

            elif request.user.tipo == "coordenador":
                if vaga.status != "aprovada":
                    vaga.status = "aprovada"
                    vaga.etapa = "publicada"
                    vaga.data_publicacao = timezone.now()
                    vaga.aprovado_por = request.user

                messages.success(
                    request,
                    "Vaga atualizada com sucesso."
                )

            vaga.save()
            return JsonResponse({"ok": True})

        # formulário inválido → devolve HTML do form
        return render(
            request,
            "dashboard/partials/vagas/_vaga_form.html",
            {
                "form": form,
                "vaga": vaga,
                "nome": "vaga",
                "erro": "Erro ao atualizar vaga.",
            },
            status=400
        )

    return render(
        request,
        "dashboard/partials/vagas/_vaga_form.html",
        {
            "form": VagaForm(instance=vaga),
            "vaga": vaga,
            "nome": "vaga",
        }
    )


# ===================== DETALHAR =====================
@login_required
def ajax_detalhar_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)

    return render(
        request,
        "dashboard/partials/vagas/_vaga_detalhe.html",
        {"vaga": vaga}
    )


# ===================== REMOVER =====================
@login_required
def ajax_remover_vaga(request, id):
    vaga = get_object_or_404(Vaga, id=id)

    if request.user.tipo == "empresa" and vaga.empresa != request.user:
        messages.error(
            request,
            "Você não tem permissão para excluir esta vaga."
        )
        return JsonResponse({"ok": False}, status=403)

    if request.method == "POST":
        vaga.delete()
        messages.success(request, "Vaga removida com sucesso.")
        return JsonResponse({"ok": True})

    return render(
        request,
        "dashboard/partials/vagas/_vaga_excluir.html",
        {"vaga": vaga}
    )


# ===================== MENSAGENS =====================
@login_required
def ajax_mensagens(request):
    return render(
        request,
        "partials/_messages.html"
    )


