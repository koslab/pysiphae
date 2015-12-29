
def make_ldapattr_plugin(url, attributes, bind_dn, bind_password):
    import ldap
    from repoze.who.plugins.ldap import LDAPAttributesPlugin
    connection = ldap.initialize(url)
    connection.bind(bind_dn,bind_password)
    return LDAPAttributesPlugin(connection, attributes)

