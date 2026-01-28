from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dbmedical.models import (
    VisitType, VisitStatus, Gestor, Doctor, Institution, Visit
)
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos de prueba...')
        
        # Crear tipos de visita
        tipo_medicos, _ = VisitType.objects.get_or_create(name='Médicos')
        tipo_instituciones, _ = VisitType.objects.get_or_create(name='Instituciones')
        self.stdout.write('✓ Tipos de visita creados')
        
        # Crear estados
        estados = [
            ('Programada', '#3788d8'),
            ('Realizada', '#28a745'),
            ('Reprogramada', '#ffc107'),
            ('Cancelada', '#dc3545'),
        ]
        for nombre, color in estados:
            VisitStatus.objects.get_or_create(name=nombre, defaults={'color': color})
        self.stdout.write('✓ Estados creados')
        
        # Crear usuarios y gestores
        gestores_data = [
            ('gestor1', 'Carlos Rodríguez', '300-123-4567'),
            ('gestor2', 'María García', '300-234-5678'),
            ('gestor3', 'Juan Martínez', '300-345-6789'),
        ]
        
        for username, name, phone in gestores_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': name.split()[0], 'last_name': name.split()[1]}
            )
            if created:
                user.set_password('password123')
                user.save()
            
            Gestor.objects.get_or_create(
                user=user,
                defaults={'name': name, 'phone': phone}
            )
        self.stdout.write('✓ Gestores creados')
        
        # Crear médicos
        medicos_data = [
            ('Juan Pérez', 'Cardiología', '311-111-1111', 'juan.perez@hospital.com'),
            ('Ana López', 'Pediatría', '311-222-2222', 'ana.lopez@clinica.com'),
            ('Carlos Gómez', 'Medicina General', '311-333-3333', 'carlos.gomez@hospital.com'),
            ('Laura Martínez', 'Neurología', '311-444-4444', 'laura.martinez@clinica.com'),
            ('Pedro Sánchez', 'Ortopedia', '311-555-5555', 'pedro.sanchez@hospital.com'),
        ]
        
        for name, specialty, phone, email in medicos_data:
            Doctor.objects.get_or_create(
                name=name,
                defaults={'specialty': specialty, 'phone': phone, 'email': email}
            )
        self.stdout.write('✓ Médicos creados')
        
        # Crear instituciones
        instituciones_data = [
            ('Hospital San José', 'Calle 10 # 20-30', '601-123-4567'),
            ('Clínica del Norte', 'Carrera 15 # 45-67', '601-234-5678'),
            ('Centro Médico Salud Plus', 'Avenida 68 # 12-34', '601-345-6789'),
            ('Hospital Santa María', 'Calle 26 # 50-10', '601-456-7890'),
        ]
        
        for name, address, phone in instituciones_data:
            Institution.objects.get_or_create(
                name=name,
                defaults={'address': address, 'phone': phone}
            )
        self.stdout.write('✓ Instituciones creadas')
        
        # Crear visitas de prueba
        gestores = list(Gestor.objects.all())
        medicos = list(Doctor.objects.all())
        instituciones = list(Institution.objects.all())
        estados = list(VisitStatus.objects.all())
        
        # Crear visitas para los próximos 30 días
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        for i in range(30):
            # 2-4 visitas por día
            num_visits = random.randint(2, 4)
            for j in range(num_visits):
                visit_date = base_date + timedelta(days=i, hours=random.randint(0, 8))
                gestor = random.choice(gestores)
                estado = random.choice(estados)
                
                # Alternar entre médicos e instituciones
                if random.choice([True, False]):
                    Visit.objects.get_or_create(
                        visit_type=tipo_medicos,
                        status=estado,
                        gestor=gestor,
                        doctor=random.choice(medicos),
                        visit_date=visit_date,
                        defaults={
                            'duration_minutes': random.choice([30, 45, 60]),
                            'objective': f'Visita de seguimiento {i+1}-{j+1}',
                            'notes': 'Visita de prueba generada automáticamente'
                        }
                    )
                else:
                    Visit.objects.get_or_create(
                        visit_type=tipo_instituciones,
                        status=estado,
                        gestor=gestor,
                        institution=random.choice(instituciones),
                        visit_date=visit_date,
                        defaults={
                            'duration_minutes': random.choice([60, 90, 120]),
                            'objective': f'Reunión institucional {i+1}-{j+1}',
                            'notes': 'Visita de prueba generada automáticamente'
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS('✓ Datos de prueba creados exitosamente'))
        self.stdout.write('')
        self.stdout.write('Credenciales de prueba:')
        self.stdout.write('  Admin: admin / (tu contraseña)')
        self.stdout.write('  Gestor 1: gestor1 / password123')
        self.stdout.write('  Gestor 2: gestor2 / password123')
        self.stdout.write('  Gestor 3: gestor3 / password123')