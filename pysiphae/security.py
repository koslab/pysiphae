def groupfinder(identity, request):
    result = []
    if 'repoze.who.userid' in identity:
        id_ = identity['repoze.who.userid']
        result.append('group:LoggedIn')
        result.append('group:%s' % id_)
    return result
