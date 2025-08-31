"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license."""

import logging
from label_studio.core.utils.params import get_env, get_bool_env

logger = logging.getLogger(__name__)

AUTH_LDAP_ENABLED = get_bool_env('AUTH_LDAP_ENABLED', False)
AUTH_LDAP_SERVER_URI = get_env('AUTH_LDAP_SERVER_URI', '')
AUTH_LDAP_BIND_DN = get_env('AUTH_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = get_env('AUTH_LDAP_BIND_PASSWORD', '')

AUTH_LDAP_CONNECTION_OPTIONS = {}
raw_options = get_env('AUTH_LDAP_CONNECTION_OPTIONS', '')
if raw_options:
    try:
        import ldap  # type: ignore
        for option in raw_options.split(';'):
            if not option:
                continue
            key, value = option.split('=', 1)
            ldap_key = getattr(ldap, key, key)
            try:
                value = int(value)
            except ValueError:
                pass
            AUTH_LDAP_CONNECTION_OPTIONS[ldap_key] = value
    except Exception:
        logger.exception('Failed to parse AUTH_LDAP_CONNECTION_OPTIONS')
