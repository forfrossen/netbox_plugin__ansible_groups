"""
Example of the inventory export format that the plugin generates.
This demonstrates the DebOps-compatible output structure.
"""

EXAMPLE_INVENTORY_OUTPUT = """
# Example inventory output from /api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/

[ungrouped]
standalone-server

[Production]

[web-servers]
web01.example.com
web02.example.com

[db-servers]
db01.example.com

[app-servers]
app01.example.com
app02.example.com

[Production:children]
web-servers
db-servers
app-servers

[Development]

[dev-web]
dev-web01.example.com

[dev-db]
dev-db01.example.com

[Development:children]
dev-web
dev-db

[Production:vars]
env=production
monitoring=enabled
backup_schedule=daily

[web-servers:vars]
role=webserver
nginx_version=1.20
ssl_enabled=true

[db-servers:vars]
role=database
mysql_version=8.0
replication=master-slave

[app-servers:vars]
role=application
java_version=11
heap_size=4g

[Development:vars]
env=development
monitoring=disabled
backup_schedule=weekly

[dev-web:vars]
role=webserver
nginx_version=1.18

[dev-db:vars]
role=database
mysql_version=8.0
"""

def demonstrate_api_usage():
    """
    Example API calls for managing Ansible groups.
    """
    examples = {
        "create_group": {
            "method": "POST",
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/",
            "data": {
                "name": "Production",
                "slug": "production",
                "description": "Production environment group",
                "variables": "env: production\nmonitoring: enabled"
            }
        },
        "list_groups": {
            "method": "GET", 
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/",
            "description": "List all groups"
        },
        "filter_by_parent": {
            "method": "GET",
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/?parent_group_id=1",
            "description": "Get all child groups of parent ID 1"
        },
        "filter_with_devices": {
            "method": "GET", 
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/?has_devices=true",
            "description": "Get groups that have devices assigned"
        },
        "search_variables": {
            "method": "GET",
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/?variables_contain=webserver", 
            "description": "Find groups with 'webserver' in variables"
        },
        "export_inventory": {
            "method": "GET",
            "url": "/api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/",
            "description": "Export complete inventory in DebOps format"
        }
    }
    
    return examples

if __name__ == "__main__":
    print("NetBox Ansible Groups Plugin - API Examples")
    print("=" * 50)
    
    examples = demonstrate_api_usage()
    for name, example in examples.items():
        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"  {example['method']} {example['url']}")
        if 'data' in example:
            import json
            print(f"  Data: {json.dumps(example['data'], indent=2)}")
        if 'description' in example:
            print(f"  Description: {example['description']}")
    
    print(f"\n\nExample Inventory Output:")
    print(EXAMPLE_INVENTORY_OUTPUT)