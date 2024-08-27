from rest_framework import routers

from applications.sakura.viewsets import CapturedCardsViewSet, CaptureCardViewSet

router = routers.SimpleRouter()

router.register(r'captured-cards', CapturedCardsViewSet, basename='captured-cards')
router.register(r'capture-card', CaptureCardViewSet, basename='capture-card')

urlpatterns = router.urls
