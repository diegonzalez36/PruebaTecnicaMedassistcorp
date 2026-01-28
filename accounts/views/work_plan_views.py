from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from datetime import datetime
from dbmedical.models import Visit, VisitType, VisitStatus, Gestor
from accounts.forms import VisitForm


@login_required
def calendar_view(request):
    """Vista principal del calendario"""
    context = {
        'statuses': VisitStatus.objects.all(),
        'gestores': Gestor.objects.all(),
    }
    return render(request, 'accounts/work_plan/calendar.html', context)


@login_required
def events_api(request):
    """API REST para obtener eventos del calendario"""
    try:
        # Obtener parámetros de filtro
        start = request.GET.get('start')
        end = request.GET.get('end')
        visit_type = request.GET.get('type')
        status = request.GET.get('status')
        gestor = request.GET.get('gestor')
        
        # Query base
        visits = Visit.objects.select_related(
            'visit_type', 'status', 'gestor', 'doctor', 'institution'
        )
        
        # Aplicar filtros
        if start:
            visits = visits.filter(visit_date__gte=start)
        if end:
            visits = visits.filter(visit_date__lte=end)
        if visit_type:
            visits = visits.filter(visit_type_id=visit_type)
        if status:
            visits = visits.filter(status_id=status)
        if gestor:
            visits = visits.filter(gestor_id=gestor)
        
        # Formatear eventos para FullCalendar
        events = []
        for visit in visits:
            events.append({
                'id': visit.id,
                'title': visit.get_title(),
                'start': visit.visit_date.isoformat(),
                'end': visit.get_end_time().isoformat(),
                'color': visit.status.color,
                'type': visit.visit_type.name.lower(),
                'status': visit.status.name,
                'url': f'/work-plan/visit/{visit.id}/',
                'extendedProps': {
                    'gestor': visit.gestor.name,
                    'objective': visit.objective or '',
                }
            })
        
        return JsonResponse(events, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET", "POST"])
def create_visit(request):
    """Crear nueva visita"""
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            try:
                visit = form.save()
                messages.success(request, 'Visita creada exitosamente.')
                return redirect('view_visit', visit_id=visit.id)
            except Exception as e:
                messages.error(request, f'Error al crear visita: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Prellenar fecha si viene en el query string
        initial = {}
        if 'date' in request.GET:
            try:
                date_str = request.GET['date']
                initial['visit_date'] = datetime.fromisoformat(date_str)
            except:
                pass
        form = VisitForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Crear Visita',
        'action': 'create'
    }
    return render(request, 'accounts/work_plan/visit_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_visit(request, visit_id):
    """Editar visita existente"""
    visit = get_object_or_404(Visit, id=visit_id)
    
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Visita actualizada exitosamente.')
                return redirect('view_visit', visit_id=visit.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar visita: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VisitForm(instance=visit)
    
    context = {
        'form': form,
        'visit': visit,
        'title': 'Editar Visita',
        'action': 'edit'
    }
    return render(request, 'accounts/work_plan/visit_form.html', context)


@login_required
def view_visit(request, visit_id):
    """Ver detalles de visita"""
    visit = get_object_or_404(
        Visit.objects.select_related('visit_type', 'status', 'gestor', 'doctor', 'institution'),
        id=visit_id
    )
    
    context = {
        'visit': visit
    }
    return render(request, 'accounts/work_plan/visit_detail.html', context)


@login_required
@require_http_methods(["POST"])
def delete_visit(request, visit_id):
    """Eliminar visita"""
    visit = get_object_or_404(Visit, id=visit_id)
    try:
        visit.delete()
        messages.success(request, 'Visita eliminada exitosamente.')
        return redirect('work_plan_calendar')
    except Exception as e:
        messages.error(request, f'Error al eliminar visita: {str(e)}')
        return redirect('view_visit', visit_id=visit_id)