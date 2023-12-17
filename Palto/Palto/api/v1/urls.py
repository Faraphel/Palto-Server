"""
Urls for the Palto project's API v1.

All the urls for every model of the API are described here.
"""


from rest_framework import routers

from . import views

app_name = "PaltoAPIv1"

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename="User")
router.register(r'departments', views.DepartmentViewSet, basename="Department")
router.register(r'student_groups', views.StudentGroupViewSet, basename="StudentGroup")
router.register(r'teaching_units', views.TeachingUnitViewSet, basename="TeachingUnit")
router.register(r'student_cards', views.StudentCardViewSet, basename="StudentCard")
router.register(r'teaching_sessions', views.TeachingSessionViewSet, basename="TeachingSession")
router.register(r'attendances', views.AttendanceViewSet, basename="Attendance")
router.register(r'absences', views.AbsenceViewSet, basename="Absence")
router.register(r'absence_attachments', views.AbsenceAttachmentViewSet, basename="AbsenceAttachment")

urlpatterns = router.urls
