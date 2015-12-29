def groupfinder(identity, request):
    result = []
    if 'repoze.who.userid' in identity:
        id_ = identity['repoze.who.userid']
        result.append('group:LoggedIn')
        result.append('group:%s' % id_)
    if 'memberOf' in identity:
        # ldap memberOf
        for group in identity['memberOf']:
            groupname = group.split(',')[0].split('=')[1]
            result.append('group:%s' % groupname)
    return result
