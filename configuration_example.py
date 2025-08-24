# NetBox Configuration Example for Ansible Groups Plugin

# Add to your NetBox configuration.py file:

# Enable the plugin
PLUGINS = [
    'netbox_ansible_groups',
    # ... other plugins
]

# Plugin configuration (optional)
PLUGINS_CONFIG = {
    'netbox_ansible_groups': {
        # Plugin settings can be added here if needed in future versions
    }
}

# Example workflow:
# 1. Install plugin: pip install netbox-ansible-groups
# 2. Add to PLUGINS list above
# 3. Run migrations: python manage.py migrate
# 4. Restart NetBox
# 5. Access via: NetBox UI > Plugins > Ansible Groups