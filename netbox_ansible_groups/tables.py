import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn
from utilities.tables import TagColumn, ActionsColumn
from .models import AnsibleGroup


class AnsibleGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    parent_group = tables.Column(
        linkify=True
    )
    child_count = tables.Column(
        accessor='child_groups.count',
        verbose_name='Child Groups'
    )
    device_count = tables.Column(
        accessor='devices.count',
        verbose_name='Devices'
    )
    vm_count = tables.Column(
        accessor='virtual_machines.count',
        verbose_name='Virtual Machines'
    )
    tags = TagColumn(
        url_name='plugins:netbox_ansible_groups:ansiblegroup_list'
    )
    actions = ActionsColumn(
        actions=('edit', 'delete')
    )

    class Meta(NetBoxTable.Meta):
        model = AnsibleGroup
        fields = (
            'pk', 'id', 'name', 'slug', 'description', 'parent_group', 
            'child_count', 'device_count', 'vm_count', 'tags', 'actions',
            'created', 'last_updated'
        )
        default_columns = (
            'pk', 'name', 'description', 'parent_group', 'child_count', 
            'device_count', 'vm_count', 'actions'
        )