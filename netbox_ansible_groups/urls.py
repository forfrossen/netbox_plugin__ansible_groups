from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views

app_name = 'netbox_ansible_groups'

urlpatterns = [
    # Ansible Groups
    path('ansible-groups/', views.AnsibleGroupListView.as_view(), name='ansiblegroup_list'),
    path('ansible-groups/add/', views.AnsibleGroupEditView.as_view(), name='ansiblegroup_add'),
    path('ansible-groups/import/', views.AnsibleGroupBulkImportView.as_view(), name='ansiblegroup_import'),
    path('ansible-groups/edit/', views.AnsibleGroupBulkEditView.as_view(), name='ansiblegroup_bulk_edit'),
    path('ansible-groups/delete/', views.AnsibleGroupBulkDeleteView.as_view(), name='ansiblegroup_bulk_delete'),
    path('ansible-groups/<int:pk>/', views.AnsibleGroupView.as_view(), name='ansiblegroup'),
    path('ansible-groups/<int:pk>/edit/', views.AnsibleGroupEditView.as_view(), name='ansiblegroup_edit'),
    path('ansible-groups/<int:pk>/delete/', views.AnsibleGroupDeleteView.as_view(), name='ansiblegroup_delete'),
    path('ansible-groups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ansiblegroup_changelog',
         kwargs={'model': models.AnsibleGroup}),
]