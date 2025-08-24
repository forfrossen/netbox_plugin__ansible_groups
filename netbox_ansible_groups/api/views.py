from netbox.api.viewsets import NetBoxModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q
import json
import yaml

from ..models import AnsibleGroup
from .serializers import AnsibleGroupSerializer
from ..filtersets import AnsibleGroupFilterSet


class AnsibleGroupViewSet(NetBoxModelViewSet):
    queryset = AnsibleGroup.objects.prefetch_related(
        'parent_group', 'child_groups', 'devices', 'virtual_machines', 'tags'
    )
    serializer_class = AnsibleGroupSerializer
    filterset_class = AnsibleGroupFilterSet

    @action(detail=False, methods=['get'])
    def export_inventory(self, request):
        """
        Export all groups as DebOps-compatible inventory in INI format.
        """
        # Get all groups
        groups = self.get_queryset()
        
        # Build inventory structure
        inventory_lines = []
        
        # Add ungrouped hosts first (devices/VMs not in any group)
        ungrouped_devices = []
        ungrouped_vms = []
        
        # Find devices and VMs that are not in any group
        from dcim.models import Device
        from virtualization.models import VirtualMachine
        
        all_devices = Device.objects.all()
        all_vms = VirtualMachine.objects.all()
        
        grouped_devices = set()
        grouped_vms = set()
        
        for group in groups:
            grouped_devices.update(group.devices.all())
            grouped_vms.update(group.virtual_machines.all())
        
        ungrouped_devices = [d for d in all_devices if d not in grouped_devices]
        ungrouped_vms = [vm for vm in all_vms if vm not in grouped_vms]
        
        # Add ungrouped section if there are any
        if ungrouped_devices or ungrouped_vms:
            inventory_lines.append("[ungrouped]")
            for device in ungrouped_devices:
                inventory_lines.append(device.name)
            for vm in ungrouped_vms:
                inventory_lines.append(vm.name)
            inventory_lines.append("")
        
        # Add each group
        for group in groups.filter(parent_group__isnull=True):  # Start with root groups
            self._add_group_to_inventory(group, inventory_lines)
        
        # Add group variables
        inventory_lines.append("")
        for group in groups:
            if group.variables:
                inventory_lines.append(f"[{group.name}:vars]")
                # Try to parse as YAML first, then JSON, then treat as plain text
                try:
                    variables = yaml.safe_load(group.variables)
                    if isinstance(variables, dict):
                        for key, value in variables.items():
                            inventory_lines.append(f"{key}={value}")
                    else:
                        # If not a dict, treat as plain text
                        for line in group.variables.split('\n'):
                            if line.strip():
                                inventory_lines.append(line.strip())
                except:
                    # If YAML parsing fails, try JSON
                    try:
                        variables = json.loads(group.variables)
                        if isinstance(variables, dict):
                            for key, value in variables.items():
                                inventory_lines.append(f"{key}={value}")
                        else:
                            for line in group.variables.split('\n'):
                                if line.strip():
                                    inventory_lines.append(line.strip())
                    except:
                        # Treat as plain text
                        for line in group.variables.split('\n'):
                            if line.strip():
                                inventory_lines.append(line.strip())
                inventory_lines.append("")
        
        inventory_content = '\n'.join(inventory_lines)
        
        response = HttpResponse(inventory_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="inventory.ini"'
        return response
    
    def _add_group_to_inventory(self, group, inventory_lines, processed=None):
        """
        Recursively add a group and its children to the inventory.
        """
        if processed is None:
            processed = set()
        
        if group.id in processed:
            return
        processed.add(group.id)
        
        # Add group header
        inventory_lines.append(f"[{group.name}]")
        
        # Add devices and VMs
        for device in group.devices.all():
            inventory_lines.append(device.name)
        for vm in group.virtual_machines.all():
            inventory_lines.append(vm.name)
        
        inventory_lines.append("")
        
        # Add children section if there are child groups
        if group.child_groups.exists():
            inventory_lines.append(f"[{group.name}:children]")
            for child in group.child_groups.all():
                inventory_lines.append(child.name)
            inventory_lines.append("")
        
        # Recursively add child groups
        for child in group.child_groups.all():
            self._add_group_to_inventory(child, inventory_lines, processed)