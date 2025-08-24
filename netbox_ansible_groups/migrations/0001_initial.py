# Generated migration for netbox_ansible_groups

from django.db import migrations, models
import django.db.models.deletion
import utilities.json
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0108_webhook_custom_field_data_webhook_tags'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('dcim', '0181_rename_180_cable_length_unit'),
        ('virtualization', '0037_virtualmachine_natural_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsibleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(help_text='Name of the Ansible group', max_length=100)),
                ('slug', models.SlugField(help_text='URL-friendly unique identifier', max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text='Optional description of the group')),
                ('variables', models.TextField(blank=True, help_text='Group variables in YAML, JSON, or plain text format')),
                ('devices', models.ManyToManyField(blank=True, help_text='Devices belonging to this group', related_name='ansible_groups', to='dcim.device')),
                ('parent_group', models.ForeignKey(blank=True, help_text='Parent group for hierarchical organization', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_groups', to='netbox_ansible_groups.ansiblegroup')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('virtual_machines', models.ManyToManyField(blank=True, help_text='Virtual machines belonging to this group', related_name='ansible_groups', to='virtualization.virtualmachine')),
            ],
            options={
                'verbose_name': 'Ansible Group',
                'verbose_name_plural': 'Ansible Groups',
                'ordering': ('name',),
            },
        ),
    ]