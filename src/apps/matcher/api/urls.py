from rest_framework import routers

# import views that will be mapped to url paths
from .views import RecordModelViewSet

router = routers.SimpleRouter()
router.register(r'', RecordModelViewSet)
urlpatterns = router.urls