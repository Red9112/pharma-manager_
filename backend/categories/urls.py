from rest_framework.routers import DefaultRouter

from .views import CategorieViewSet

router = DefaultRouter()
router.register("", CategorieViewSet, basename="categorie")

urlpatterns = router.urls

