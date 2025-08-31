"""LDAP configuration for Label Studio."""

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, GroupOfNamesType, PosixGroupType

from core.utils.params import get_env, get_bool_env


# Basic connection settings
AUTH_LDAP_SERVER_URI = get_env('AUTH_LDAP_SERVER_URI', '')
AUTH_LDAP_BIND_DN = get_env('AUTH_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = get_env('AUTH_LDAP_BIND_PASSWORD', '')


# User search configuration
AUTH_LDAP_USER_DN_TEMPLATE = get_env('AUTH_LDAP_USER_DN_TEMPLATE', '')
_user_search_bases = [b for b in get_env('AUTH_LDAP_USER_SEARCH_BASES', '').split(';') if b]
AUTH_LDAP_USER_QUERY_FIELD = get_env('AUTH_LDAP_USER_QUERY_FIELD', 'email')
if _user_search_bases:
    _searches = [
        LDAPSearch(base, ldap.SCOPE_SUBTREE, f'({AUTH_LDAP_USER_QUERY_FIELD}=%(user)s)')
        for base in _user_search_bases
    ]
    AUTH_LDAP_USER_SEARCH = _searches[0] if len(_searches) == 1 else LDAPSearchUnion(*_searches)


# Optional user attribute mapping
AUTH_LDAP_USER_ATTR_MAP = {}
for env_name, attr in [
    ('AUTH_LDAP_USER_ATTR_MAP_FIRST_NAME', 'first_name'),
    ('AUTH_LDAP_USER_ATTR_MAP_LAST_NAME', 'last_name'),
    ('AUTH_LDAP_USER_ATTR_MAP_EMAIL', 'email'),
    ('AUTH_LDAP_USER_ATTR_MAP_USERNAME', 'username'),
]:
    value = get_env(env_name)
    if value:
        AUTH_LDAP_USER_ATTR_MAP[attr] = value


# Group search configuration
_group_base = get_env('AUTH_LDAP_GROUP_SEARCH_BASE_DN')
_group_filter = get_env('AUTH_LDAP_GROUP_SEARCH_FILTER_STR')
if _group_base and _group_filter:
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(_group_base, ldap.SCOPE_SUBTREE, _group_filter)
    _group_type = get_env('AUTH_LDAP_GROUP_TYPE', '').lower()
    AUTH_LDAP_GROUP_TYPE = PosixGroupType() if _group_type == 'posix' else GroupOfNamesType()


# TLS and connection options
AUTH_LDAP_START_TLS = get_bool_env('AUTH_LDAP_START_TLS', False)
AUTH_LDAP_CONNECTION_OPTIONS = {}
for item in get_env('AUTH_LDAP_CONNECTION_OPTIONS', '').split(';'):
    if not item:
        continue
    key, _, value = item.partition('=')
    if hasattr(ldap, key) and value:
        AUTH_LDAP_CONNECTION_OPTIONS[getattr(ldap, key)] = value

