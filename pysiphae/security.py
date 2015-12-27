def groupfinder(identity, request):
    result = []
    if 'repoze.who.userid' in identity:
        result.append('group:LoggedIn')
    return result
