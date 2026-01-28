from django.contrib import admin
from .models import VisitType, VisitStatus, Gestor, Doctor, Institution, Visit


@admin.register(VisitType)
class VisitTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(VisitStatus)
class VisitStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color']


@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'phone']
    search_fields = ['name', 'user__username']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialty', 'phone', 'email']
    search_fields = ['name', 'specialty']


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone']
    search_fields = ['name']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_title', 'visit_type', 'status', 'gestor', 'visit_date']
    list_filter = ['visit_type', 'status', 'gestor']
    search_fields = ['doctor__name', 'institution__name', 'objective']
    date_hierarchy = 'visit_date'