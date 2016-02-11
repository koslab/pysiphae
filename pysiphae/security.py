import re

def groupfinder(identity, request):
    if not identity:
        return ['Anonymous']

    result = []
    if 'repoze.who.userid' in identity:
        userid = identity['repoze.who.userid']
        result.append('group:LoggedIn')
        if re.match(r'(\w+=.+,?)+', userid):
            userid = userid.split(',')[0].split('=')[1]
        result.append('user:%s' % userid)
    if 'memberOf' in identity:
        # ldap memberOf
        for group in identity['memberOf']:
            groupname = group.split(',')[0].split('=')[1]
            result.append('group:%s' % groupname)
    # append from settings override
    settings = request.registry.settings
    for entry in settings['pysiphae'].get('roles', []):
        if entry['user'] == identity['repoze.who.userid']:
            result += entry['principals']
    return result
