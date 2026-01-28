from django.urls import path
from accounts.views import (
    calendar_view,
    events_api,
    create_visit,
    edit_visit,
    view_visit,
    delete_visit
)

urlpatterns = [
    path('work-plan/', calendar_view, name='work_plan_calendar'),
    path('api/work-plan/events/', events_api, name='work_plan_events_api'),
    path('work-plan/create/', create_visit, name='create_visit'),
    path('work-plan/edit/<int:visit_id>/', edit_visit, name='edit_visit'),
    path('work-plan/visit/<int:visit_id>/', view_visit, name='view_visit'),
    path('work-plan/delete/<int:visit_id>/', delete_visit, name='delete_visit'),
]