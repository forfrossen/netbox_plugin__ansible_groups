"""
Test file to demonstrate the NetBox Ansible Groups plugin functionality.

This plugin provides:
1. AnsibleGroup model with hierarchical structure
2. Many-to-many relationships with Devices and VirtualMachines  
3. REST API with filtering capabilities
4. Export functionality for DebOps-compatible inventory
5. Web interface for managing groups

Example usage:

# Create a root group
root_group = AnsibleGroup.objects.create(
    name="Production",
    slug="production",
    description="Production environment group",
    variables="env: production\nmonitoring: enabled"
)

# Create child groups
web_group = AnsibleGroup.objects.create(
    name="Web Servers",
    slug="web-servers", 
    parent_group=root_group,
    variables="role: webserver\nnginx_version: 1.20"
)

db_group = AnsibleGroup.objects.create(
    name="Database Servers",
    slug="db-servers",
    parent_group=root_group, 
    variables="role: database\nmysql_version: 8.0"
)

# Assign devices to groups
web_group.devices.add(device1, device2)
db_group.devices.add(device3)

# Export inventory via API
GET /api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/

# This will return DebOps-compatible INI format:
[Production]

[web-servers]
device1
device2

[db-servers] 
device3

[Production:children]
web-servers
db-servers

[Production:vars]
env=production
monitoring=enabled

[web-servers:vars]
role=webserver
nginx_version=1.20

[db-servers:vars]
role=database
mysql_version=8.0
"""

def test_plugin_structure():
    """
    Test that all required plugin components are present.
    """
    import os
    
    base_path = '/home/runner/work/netbox_plugin__ansible_groups/netbox_plugin__ansible_groups/netbox_ansible_groups'
    
    required_files = [
        '__init__.py',
        'models.py', 
        'views.py',
        'urls.py',
        'forms.py',
        'tables.py',
        'filtersets.py',
        'navigation.py',
        'api/__init__.py',
        'api/serializers.py',
        'api/views.py', 
        'api/urls.py',
        'migrations/__init__.py',
        'migrations/0001_initial.py',
        'templates/netbox_ansible_groups/ansiblegroup.html'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path), f"Missing required file: {file_path}"
    
    print("✓ All required plugin files are present")

if __name__ == "__main__":
    test_plugin_structure()
    print("✓ Plugin structure validation complete")