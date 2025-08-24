from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu
from utilities.choices import ButtonColorChoices

menu = PluginMenu(
    label='Ansible Groups',
    groups=(
        ('Groups', (
            PluginMenuItem(
                link='plugins:netbox_ansible_groups:ansiblegroup_list',
                link_text='Ansible Groups',
                buttons=(
                    PluginMenuButton(
                        link='plugins:netbox_ansible_groups:ansiblegroup_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                        color=ButtonColorChoices.GREEN
                    ),
                    PluginMenuButton(
                        link='plugins:netbox_ansible_groups:ansiblegroup_import',
                        title='Import',
                        icon_class='mdi mdi-upload',
                        color=ButtonColorChoices.CYAN
                    ),
                )
            ),
        )),
    )
)