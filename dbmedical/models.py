from django.db import models
from django.contrib.auth.models import User


class VisitType(models.Model):
    """Tipo de visita: Médicos o Instituciones"""
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'visit_types'
        verbose_name = 'Tipo de Visita'
        verbose_name_plural = 'Tipos de Visita'
    
    def __str__(self):
        return self.name


class VisitStatus(models.Model):
    """Estado de la visita"""
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, help_text='Color hexadecimal, ej: #3788d8')
    
    class Meta:
        db_table = 'visit_statuses'
        verbose_name = 'Estado de Visita'
        verbose_name_plural = 'Estados de Visita'
    
    def __str__(self):
        return self.name


class Gestor(models.Model):
    """Gestor/Representante que realiza las visitas"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'gestores'
        verbose_name = 'Gestor'
        verbose_name_plural = 'Gestores'
    
    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Médico a visitar"""
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
    
    def __str__(self):
        return self.name


class Institution(models.Model):
    """Institución médica a visitar"""
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'institutions'
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
    
    def __str__(self):
        return self.name


class Visit(models.Model):
    """Visita médica o institucional"""
    visit_type = models.ForeignKey(VisitType, on_delete=models.PROTECT)
    status = models.ForeignKey(VisitStatus, on_delete=models.PROTECT)
    gestor = models.ForeignKey(Gestor, on_delete=models.CASCADE)
    
    # Relaciones opcionales (una visita es O a médico O a institución)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    
    # Detalles de la visita
    visit_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    objective = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'visits'
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-visit_date']
    
    def __str__(self):
        if self.doctor:
            return f"Visita - Dr. {self.doctor.name} - {self.visit_date.strftime('%d/%m/%Y')}"
        elif self.institution:
            return f"Visita - {self.institution.name} - {self.visit_date.strftime('%d/%m/%Y')}"
        return f"Visita {self.id}"
    
    def get_title(self):
        """Título para mostrar en el calendario"""
        if self.doctor:
            return f"Visita - Dr. {self.doctor.name}"
        elif self.institution:
            return f"Visita - {self.institution.name}"
        return "Visita"
    
    def get_end_time(self):
        """Calcula la hora de fin basado en la duración"""
        from datetime import timedelta
        return self.visit_date + timedelta(minutes=self.duration_minutes)