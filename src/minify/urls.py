from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("services", views.ServiceViewSet)
router.register("links", views.LinkViewSet)

urlpatterns = router.urls
