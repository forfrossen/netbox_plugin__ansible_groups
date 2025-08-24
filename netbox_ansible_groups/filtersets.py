import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import AnsibleGroup


class AnsibleGroupFilterSet(NetBoxModelFilterSet):
    parent_group_id = django_filters.ModelMultipleChoiceFilter(
        queryset=AnsibleGroup.objects.all(),
        label='Parent group (ID)',
    )
    parent_group = django_filters.ModelMultipleChoiceFilter(
        field_name='parent_group__slug',
        queryset=AnsibleGroup.objects.all(),
        to_field_name='slug',
        label='Parent group (slug)',
    )
    has_children = django_filters.BooleanFilter(
        method='filter_has_children',
        label='Has child groups',
    )
    has_devices = django_filters.BooleanFilter(
        method='filter_has_devices',
        label='Has devices',
    )
    has_virtual_machines = django_filters.BooleanFilter(
        method='filter_has_virtual_machines',
        label='Has virtual machines',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=None,  # Will be set in __init__
        label='Device (ID)',
    )
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machines',
        queryset=None,  # Will be set in __init__
        label='Virtual Machine (ID)',
    )
    variables_contain = django_filters.CharFilter(
        method='filter_variables_contain',
        label='Variables contain (wildcard)',
    )
    variable_name = django_filters.CharFilter(
        method='filter_variable_name',
        label='Has variable name',
    )

    class Meta:
        model = AnsibleGroup
        fields = ['id', 'name', 'slug', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set querysets for device and VM filters
        from dcim.models import Device
        from virtualization.models import VirtualMachine
        
        self.filters['device_id'].queryset = Device.objects.all()
        self.filters['virtual_machine_id'].queryset = VirtualMachine.objects.all()

    def filter_has_children(self, queryset, name, value):
        if value:
            return queryset.filter(child_groups__isnull=False).distinct()
        else:
            return queryset.filter(child_groups__isnull=True)

    def filter_has_devices(self, queryset, name, value):
        if value:
            return queryset.filter(devices__isnull=False).distinct()
        else:
            return queryset.filter(devices__isnull=True)

    def filter_has_virtual_machines(self, queryset, name, value):
        if value:
            return queryset.filter(virtual_machines__isnull=False).distinct()
        else:
            return queryset.filter(virtual_machines__isnull=True)

    def filter_variables_contain(self, queryset, name, value):
        """
        Filter groups where variables field contains the specified text (case-insensitive).
        """
        return queryset.filter(variables__icontains=value)

    def filter_variable_name(self, queryset, name, value):
        """
        Filter groups that have a specific variable name defined.
        This is a simple implementation that looks for the variable name as a key.
        """
        # Look for patterns like "varname:" (YAML) or "varname"= (INI) or "varname": (JSON)
        patterns = [
            f'{value}:',  # YAML style
            f'{value}=',  # INI style  
            f'"{value}":',  # JSON style with quotes
            f"'{value}':",  # JSON style with single quotes
        ]
        
        q_objects = Q()
        for pattern in patterns:
            q_objects |= Q(variables__icontains=pattern)
        
        return queryset.filter(q_objects)