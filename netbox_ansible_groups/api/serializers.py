from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import AnsibleGroup


class AnsibleGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_ansible_groups-api:ansiblegroup-detail'
    )
    parent_group = serializers.PrimaryKeyRelatedField(
        queryset=AnsibleGroup.objects.all(),
        required=False,
        allow_null=True
    )
    child_groups = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    devices = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    virtual_machines = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = AnsibleGroup
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'description', 'variables',
            'parent_group', 'child_groups', 'devices', 'virtual_machines',
            'tags', 'custom_fields', 'created', 'last_updated',
        ]


class NestedAnsibleGroupSerializer(serializers.ModelSerializer):
    """
    Nested serializer for representing AnsibleGroup in related objects.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_ansible_groups-api:ansiblegroup-detail'
    )

    class Meta:
        model = AnsibleGroup
        fields = ['id', 'url', 'display', 'name', 'slug']