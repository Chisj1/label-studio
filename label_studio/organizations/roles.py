"""Role definitions and allowed actions for organizations and projects.

This module defines the available roles within Label Studio along with
permissions they grant.  The definitions are structured so they can be used
in database migrations in the future.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, List

from label_studio.core.permissions import AllPermissions, all_permissions


class RoleScope(str, Enum):
    """Scope of a role: organization-wide or project-specific."""

    ORGANIZATION = "organization"
    PROJECT = "project"


@dataclass(frozen=True)
class RoleDefinition:
    """Definition of a role and the permissions it grants."""

    name: str
    scope: RoleScope
    permissions: List[str]


# Collect all permission names for convenience when declaring wide-scope roles
_ALL_PERMISSION_NAMES: List[str] = [perm for _, perm in all_permissions]


# Individual role definitions.  These are intended to be migration ready so they
# can be inserted into the database as-is in a future migration.
ROLE_DEFINITIONS: List[RoleDefinition] = [
    # Organization scoped roles
    RoleDefinition(
        name="owner",
        scope=RoleScope.ORGANIZATION,
        permissions=_ALL_PERMISSION_NAMES,
    ),
    RoleDefinition(
        name="admin",
        scope=RoleScope.ORGANIZATION,
        permissions=[
            all_permissions.organizations_view,
            all_permissions.organizations_change,
            all_permissions.organizations_invite,
            all_permissions.projects_create,
            all_permissions.projects_view,
            all_permissions.projects_change,
            all_permissions.projects_delete,
            all_permissions.webhooks_change,
        ],
    ),
    # Project scoped roles
    RoleDefinition(
        name="manager",
        scope=RoleScope.PROJECT,
        permissions=[
            all_permissions.projects_view,
            all_permissions.projects_change,
            all_permissions.tasks_view,
            all_permissions.tasks_change,
            all_permissions.annotations_view,
            all_permissions.annotations_change,
            all_permissions.labels_view,
            all_permissions.labels_change,
        ],
    ),
    RoleDefinition(
        name="annotator",
        scope=RoleScope.PROJECT,
        permissions=[
            all_permissions.tasks_view,
            all_permissions.annotations_create,
            all_permissions.annotations_view,
            all_permissions.annotations_change,
        ],
    ),
    RoleDefinition(
        name="reviewer",
        scope=RoleScope.PROJECT,
        permissions=[
            all_permissions.tasks_view,
            all_permissions.annotations_view,
            all_permissions.annotations_change,
        ],
    ),
]


# Convenience lookups for migrations or runtime usage
ROLE_REGISTRY: Dict[str, RoleDefinition] = {role.name: role for role in ROLE_DEFINITIONS}
ROLE_CHOICES: List[tuple[str, str]] = [(role.name, role.name) for role in ROLE_DEFINITIONS]


def iter_permissions(role_name: str) -> Iterable[str]:
    """Yield permission strings for the given role name."""

    return iter(ROLE_REGISTRY[role_name].permissions)

