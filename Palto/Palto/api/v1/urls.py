from rest_framework import routers

from .views import (UserViewSet, AbsenceAttachmentViewSet, AbsenceViewSet, AttendanceViewSet, TeachingSessionViewSet,
                    StudentCardViewSet, TeachingUnitViewSet, StudentGroupViewSet, DepartmentViewSet)

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename="User")
router.register(r'departments', DepartmentViewSet, basename="Department")
router.register(r'student_groups', StudentGroupViewSet, basename="StudentGroup")
router.register(r'teaching_units', TeachingUnitViewSet, basename="TeachingUnit")
router.register(r'student_cards', StudentCardViewSet, basename="StudentCard")
router.register(r'teaching_sessions', TeachingSessionViewSet, basename="TeachingSession")
router.register(r'attendances', AttendanceViewSet, basename="Attendance")
router.register(r'absences', AbsenceViewSet, basename="Absence")
router.register(r'absence_attachments', AbsenceAttachmentViewSet, basename="AbsenceAttachment")


urlpatterns = router.urls
