from .views import get_menu

def menu_context(request):
    if request.user.is_authenticated:
        return {"menu": get_menu(request.user)}
    return {"menu": []}
