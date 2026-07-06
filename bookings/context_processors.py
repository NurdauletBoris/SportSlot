def favorites_count(request):
    if request.user.is_authenticated:
        count = request.user.favorites.count()
    else:
        count = 0
    return {'favorites_count': count}