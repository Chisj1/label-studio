# Role-Based Access Control

Label Studio uses role-based access control (RBAC) to manage what each user can see and modify.

## Roles

- **Owner** – full control over the workspace and organization settings.
- **Administrator** – manage members and configure projects.
- **Manager** – create projects and manage labeling tasks.
- **Reviewer** – review and approve completed annotations.
- **Annotator** – label data assigned to them.

## Permissions

Common permissions include:

- `organizations.view` – read organization details.
- `organizations.change` – update organization settings or membership.
- `projects.create` – create new projects.
- `projects.view` – view project data.

## Example Usage

An annotator can list organization members but cannot delete another member. A DELETE request to the memberships endpoint returns **403 Forbidden** for unauthorized roles:

```http
DELETE /api/organizations/{org_id}/memberships/{user_id}/
# -> 403 Forbidden
```

Use roles and permissions to limit access to critical actions and keep your workspace secure.
