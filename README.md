# NetBox Ansible Groups Plugin

A NetBox plugin for managing Ansible groups as first-class objects, designed to use NetBox as a Single Source of Truth for DebOps/Ansible configurations.

## Features

### 1. Ansible Group Model
- **AnsibleGroup** model with the following attributes:
  - `name` (str) - Human-readable group name
  - `slug` (str, unique) - URL-friendly identifier
  - `description` (optional, text) - Group description  
  - `variables` (multiline string) - Group variables in YAML/JSON/text format
  - `parent_group` (ForeignKey to self) - Hierarchical group nesting
- Tags support for additional categorization
- Parent-child hierarchy similar to organizational structures

### 2. Device and VM Assignments
- Many-to-many relationships with Devices and VirtualMachines
- Bi-directional filtering capabilities
- Groups can contain both physical devices and virtual machines

### 3. REST API & Filtering
- Full CRUD API for AnsibleGroup management
- Advanced filtering options:
  - Filter by group, parent, children
  - Filter across nested group hierarchies
  - Filter by contained devices/VMs
  - Filter by variable names (wildcard support)
  - Boolean filters for has_children, has_devices, has_virtual_machines

### 4. DebOps Export Function
- Export API endpoint: `/api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/`
- Generates DebOps-compatible inventory in INI format
- Includes group hierarchies, variables, and host assignments
- Supports nested group structures with `:children` sections

### 5. Web Interface
- List, create, edit, and delete groups through NetBox UI
- Hierarchical display of group relationships
- Device and VM assignment interface
- Bulk operations support

## Installation

1. Install the plugin:
```bash
pip install netbox-ansible-groups
```

2. Add to NetBox configuration in `configuration.py`:
```python
PLUGINS = [
    'netbox_ansible_groups',
]
```

3. Run migrations:
```bash
python manage.py migrate
```

## Usage Examples

### Creating Groups via API

```bash
# Create a root group
curl -X POST http://netbox/api/plugins/netbox-ansible-groups/ansible-groups/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production",
    "slug": "production", 
    "description": "Production environment",
    "variables": "env: production\nmonitoring: enabled"
  }'

# Create child group
curl -X POST http://netbox/api/plugins/netbox-ansible-groups/ansible-groups/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Web Servers",
    "slug": "web-servers",
    "parent_group": 1,
    "variables": "role: webserver\nnginx_version: 1.20"
  }'
```

### Filtering Groups

```bash
# Filter by parent group
GET /api/plugins/netbox-ansible-groups/ansible-groups/?parent_group_id=1

# Filter groups with devices
GET /api/plugins/netbox-ansible-groups/ansible-groups/?has_devices=true

# Filter by variable content
GET /api/plugins/netbox-ansible-groups/ansible-groups/?variables_contain=webserver

# Filter by variable name
GET /api/plugins/netbox-ansible-groups/ansible-groups/?variable_name=role
```

### Exporting Inventory

```bash
# Export complete inventory
curl http://netbox/api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/
```

Example output:
```ini
[ungrouped]
orphaned-device

[Production]

[web-servers]
web01
web02

[db-servers]
db01

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
```

## Compatibility

- **NetBox Version**: v4.3.1+
- **Python**: 3.8+
- **Django**: Compatible with NetBox's Django version
- **DebOps**: Compatible with DebOps dynamic inventory format

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/plugins/netbox-ansible-groups/ansible-groups/` | GET, POST | List/create groups |
| `/api/plugins/netbox-ansible-groups/ansible-groups/{id}/` | GET, PUT, PATCH, DELETE | Group details |
| `/api/plugins/netbox-ansible-groups/ansible-groups/export_inventory/` | GET | Export inventory |

## Development

The plugin follows NetBox plugin development standards:
- Uses NetBox's plugin architecture
- Leverages Django models and views
- Implements NetBox's filtering system
- Follows NetBox UI/UX patterns

## License

Apache 2.0 License
