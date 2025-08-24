from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from netbox.models import NetBoxModel
from netbox.models.features import TagsMixin
from dcim.models import Device
from virtualization.models import VirtualMachine


class AnsibleGroup(NetBoxModel, TagsMixin):
    """
    Model representing an Ansible group that can contain devices and virtual machines.
    """
    name = models.CharField(
        max_length=100,
        help_text="Name of the Ansible group"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly unique identifier"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of the group"
    )
    variables = models.TextField(
        blank=True,
        help_text="Group variables in YAML, JSON, or plain text format"
    )
    parent_group = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='child_groups',
        help_text="Parent group for hierarchical organization"
    )
    devices = models.ManyToManyField(
        Device,
        blank=True,
        related_name='ansible_groups',
        help_text="Devices belonging to this group"
    )
    virtual_machines = models.ManyToManyField(
        VirtualMachine,
        blank=True,
        related_name='ansible_groups',
        help_text="Virtual machines belonging to this group"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ansible Group'
        verbose_name_plural = 'Ansible Groups'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_ansible_groups:ansiblegroup', args=[self.pk])

    def clean(self):
        super().clean()
        
        # Ensure slug is generated if not provided
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        
        # Prevent circular parent relationships
        if self.parent_group:
            parent = self.parent_group
            while parent:
                if parent == self:
                    raise ValidationError("Circular parent relationship detected")
                parent = parent.parent_group

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def all_children(self):
        """
        Return all descendant groups (recursive).
        """
        children = list(self.child_groups.all())
        for child in list(children):
            children.extend(child.all_children)
        return children

    @property
    def all_devices(self):
        """
        Return all devices including those from child groups.
        """
        devices = list(self.devices.all())
        for child in self.all_children:
            devices.extend(child.devices.all())
        return list(set(devices))  # Remove duplicates

    @property
    def all_virtual_machines(self):
        """
        Return all virtual machines including those from child groups.
        """
        vms = list(self.virtual_machines.all())
        for child in self.all_children:
            vms.extend(child.virtual_machines.all())
        return list(set(vms))  # Remove duplicates