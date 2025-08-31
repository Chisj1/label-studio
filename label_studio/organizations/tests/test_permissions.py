from organizations.tests.factories import OrganizationFactory
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory


class TestOrganizationPermissions(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organization = OrganizationFactory(created_by__username='owner')
        cls.owner = cls.organization.created_by
        cls.member = UserFactory(username='member', active_organization=cls.organization)
        cls.outsider_org = OrganizationFactory()
        cls.outsider = UserFactory(username='outsider', active_organization=cls.outsider_org)
        cls.target = UserFactory(username='target', active_organization=cls.organization)

    def membership_url(self, user_id):
        return f'/api/organizations/{self.organization.id}/memberships/{user_id}/'

    def organization_url(self):
        return f'/api/organizations/{self.organization.id}'

    def test_non_owner_cannot_delete_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.delete(self.membership_url(self.target.id))
        assert response.status_code == 403

    def test_outsider_cannot_update_organization(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.patch(self.organization_url(), {'title': 'new title'}, format='json')
        assert response.status_code == 403
