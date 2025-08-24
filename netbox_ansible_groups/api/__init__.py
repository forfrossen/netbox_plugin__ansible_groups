from rest_framework.routers import APIRootView
from ..models import AnsibleGroup


class AnsibleGroupsRootView(APIRootView):
    """
    API root view for the ansible-groups plugin.
    """
    def get_view_name(self):
        return 'Ansible Groups'


__all__ = [
    'AnsibleGroupsRootView',
]