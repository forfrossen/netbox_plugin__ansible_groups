from netbox.plugins import PluginConfig

class NetBoxAnsibleGroupsConfig(PluginConfig):
    name = 'netbox_ansible_groups'
    verbose_name = 'NetBox Ansible Groups'
    description = 'Manage Ansible groups as first-class objects in NetBox'
    version = '0.1.0'
    author = 'forfrossen'
    author_email = ''
    base_url = 'ansible-groups'
    required_settings = []
    default_settings = {}
    
    def ready(self):
        super().ready()

config = NetBoxAnsibleGroupsConfig