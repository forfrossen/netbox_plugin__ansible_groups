from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from . import filtersets, forms, models, tables


class AnsibleGroupListView(generic.ObjectListView):
    queryset = models.AnsibleGroup.objects.all()
    table = tables.AnsibleGroupTable
    filterset = filtersets.AnsibleGroupFilterSet
    filterset_form = forms.AnsibleGroupFilterForm


class AnsibleGroupView(generic.ObjectView):
    queryset = models.AnsibleGroup.objects.all()

    def get_extra_context(self, request, instance):
        # Add related devices and VMs to context
        return {
            'devices': instance.devices.all(),
            'virtual_machines': instance.virtual_machines.all(),
            'child_groups': instance.child_groups.all(),
        }


class AnsibleGroupEditView(generic.ObjectEditView):
    queryset = models.AnsibleGroup.objects.all()
    form = forms.AnsibleGroupForm


class AnsibleGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.AnsibleGroup.objects.all()


class AnsibleGroupBulkImportView(generic.BulkImportView):
    queryset = models.AnsibleGroup.objects.all()
    model_form = forms.AnsibleGroupForm


class AnsibleGroupBulkEditView(generic.BulkEditView):
    queryset = models.AnsibleGroup.objects.all()
    filterset = filtersets.AnsibleGroupFilterSet
    table = tables.AnsibleGroupTable
    form = forms.AnsibleGroupForm


class AnsibleGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.AnsibleGroup.objects.all()
    filterset = filtersets.AnsibleGroupFilterSet
    table = tables.AnsibleGroupTable