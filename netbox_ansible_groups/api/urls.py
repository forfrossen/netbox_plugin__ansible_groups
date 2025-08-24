from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_ansible_groups-api'

router = NetBoxRouter()
router.register('ansible-groups', views.AnsibleGroupViewSet)

urlpatterns = router.urls