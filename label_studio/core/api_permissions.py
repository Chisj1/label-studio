from rest_framework.permissions import SAFE_METHODS, BasePermission

from organizations.models import Organization
from projects.models import Project


class HasObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.has_permission(request.user)


class MemberHasOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS and not request.user.own_organization:
            return False

        return obj.has_permission(request.user)


class RolePermission(BasePermission):
    """Role based permission for organization and project level operations.

    Views using this permission should define ``required_roles`` attribute with
    allowed roles for organization and/or project levels, for example::

        required_roles = {
            'organization': ['owner'],
            'project': ['owner', 'member'],
        }

    ``organization`` and ``project`` keys are optional. If ``required_roles`` is
    missing the check is skipped.
    """

    def has_permission(self, request, view):  # type: ignore[override]
        roles = getattr(view, 'required_roles', None)
        return self._check_roles(request, view, roles)

    def has_object_permission(self, request, view, obj):  # type: ignore[override]
        roles = getattr(view, 'required_roles', None)
        return self._check_roles(request, view, roles, obj=obj)

    def _check_roles(self, request, view, roles, obj=None):
        if not roles:
            return True

        user = request.user

        if roles.get('organization'):
            organization = self._get_organization(request, view, obj)
            if organization is None:
                return False
            org_role = self._get_organization_role(user, organization)
            if org_role not in roles['organization']:
                return False

        if roles.get('project'):
            project = self._get_project(request, view, obj)
            if project is None:
                return False
            project_role = self._get_project_role(user, project)
            if project_role not in roles['project']:
                return False

        return True

    def _get_organization(self, request, view, obj):
        if isinstance(obj, Organization):
            return obj
        if isinstance(obj, Project):
            return obj.organization
        if hasattr(obj, 'organization'):
            return obj.organization

        org_pk = view.kwargs.get('pk') or view.kwargs.get('organization_pk') or view.kwargs.get('id')
        if org_pk:
            try:
                return Organization.objects.get(pk=org_pk)
            except Organization.DoesNotExist:
                return None

        return request.user.active_organization

    def _get_project(self, request, view, obj):
        if isinstance(obj, Project):
            return obj
        if hasattr(obj, 'project'):
            return obj.project

        project_pk = view.kwargs.get('pk') or view.kwargs.get('project_pk') or view.kwargs.get('id')
        if project_pk:
            try:
                return Project.objects.get(pk=project_pk)
            except Project.DoesNotExist:
                return None

        return None

    @staticmethod
    def _get_organization_role(user, organization):
        if organization.created_by_id == user.id:
            return 'owner'
        if organization.has_user(user):
            return 'member'
        return 'none'

    @staticmethod
    def _get_project_role(user, project):
        if project.created_by_id == user.id:
            return 'owner'
        if project.members.filter(user=user, enabled=True).exists():
            return 'member'
        return 'none'
