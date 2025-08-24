from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import TagFilterField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import NumberWithOptions
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import AnsibleGroup


class AnsibleGroupForm(NetBoxModelForm):
    parent_group = DynamicModelChoiceField(
        queryset=AnsibleGroup.objects.all(),
        required=False,
        help_text="Parent group for hierarchical organization"
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        help_text="Devices belonging to this group"
    )
    virtual_machines = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        help_text="Virtual machines belonging to this group"
    )

    class Meta:
        model = AnsibleGroup
        fields = [
            'name', 'slug', 'description', 'variables', 'parent_group', 
            'devices', 'virtual_machines', 'tags'
        ]
        widgets = {
            'variables': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing an existing group, exclude it from parent choices to prevent circular references
        if self.instance and self.instance.pk:
            # Exclude self and all descendants
            excluded_ids = [self.instance.pk]
            excluded_ids.extend([child.pk for child in self.instance.all_children])
            self.fields['parent_group'].queryset = AnsibleGroup.objects.exclude(pk__in=excluded_ids)


class AnsibleGroupFilterForm(NetBoxModelFilterSetForm):
    model = AnsibleGroup
    fieldsets = (
        (None, ('q', 'tags')),
        ('Attributes', ('parent_group_id', 'has_children', 'has_devices', 'has_virtual_machines')),
        ('Variables', ('variables_contain', 'variable_name')),
    )
    
    parent_group_id = DynamicModelMultipleChoiceField(
        queryset=AnsibleGroup.objects.all(),
        required=False,
        label='Parent group'
    )
    has_children = forms.NullBooleanField(
        required=False,
        label='Has child groups',
        widget=forms.Select(choices=[
            ('', '-------'),
            (True, 'Yes'),
            (False, 'No'),
        ])
    )
    has_devices = forms.NullBooleanField(
        required=False,
        label='Has devices',
        widget=forms.Select(choices=[
            ('', '-------'),
            (True, 'Yes'),
            (False, 'No'),
        ])
    )
    has_virtual_machines = forms.NullBooleanField(
        required=False,
        label='Has virtual machines',
        widget=forms.Select(choices=[
            ('', '-------'),
            (True, 'Yes'),
            (False, 'No'),
        ])
    )
    variables_contain = forms.CharField(
        required=False,
        label='Variables contain',
        help_text='Search for text within variables'
    )
    variable_name = forms.CharField(
        required=False,
        label='Has variable name',
        help_text='Filter by variable name'
    )
    tags = TagFilterField(model)