document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    
    // Inicializar FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },
        height: 'auto',
        navLinks: true,
        editable: false,
        dayMaxEvents: true,
        
        // Cargar eventos desde la API
        events: function(info, successCallback, failureCallback) {
            fetchEvents(info.startStr, info.endStr, successCallback, failureCallback);
        },
        
        // Click en un evento
        eventClick: function(info) {
            info.jsEvent.preventDefault();
            if (info.event.url) {
                window.location.href = info.event.url;
            }
        },
        
        // Click en una fecha
        dateClick: function(info) {
            // Redirigir a crear visita con la fecha preseleccionada
            const date = info.dateStr + 'T09:00';
            window.location.href = `/work-plan/create/?date=${date}`;
        },
        
        // Estilo de eventos
        eventDidMount: function(info) {
            // Añadir tooltip
            info.el.title = `${info.event.title}\nEstado: ${info.event.extendedProps.status}\nGestor: ${info.event.extendedProps.gestor}`;
        }
    });
    
    calendar.render();
    
    // Función para obtener eventos
    function fetchEvents(start, end, successCallback, failureCallback) {
        const type = document.getElementById('filter-type').value;
        const status = document.getElementById('filter-status').value;
        const gestor = document.getElementById('filter-gestor').value;
        
        let url = `/api/work-plan/events/?start=${start}&end=${end}`;
        if (type) url += `&type=${type}`;
        if (status) url += `&status=${status}`;
        if (gestor) url += `&gestor=${gestor}`;
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al cargar eventos');
                }
                return response.json();
            })
            .then(data => {
                successCallback(data);
            })
            .catch(error => {
                console.error('Error:', error);
                failureCallback(error);
                alert('Error al cargar los eventos. Por favor, recargue la página.');
            });
    }
    
    // Event listeners para filtros
    document.getElementById('filter-type').addEventListener('change', function() {
        calendar.refetchEvents();
    });
    
    document.getElementById('filter-status').addEventListener('change', function() {
        calendar.refetchEvents();
    });
    
    document.getElementById('filter-gestor').addEventListener('change', function() {
        calendar.refetchEvents();
    });
    
    // Limpiar filtros
    document.getElementById('clear-filters').addEventListener('click', function() {
        document.getElementById('filter-type').value = '';
        document.getElementById('filter-status').value = '';
        document.getElementById('filter-gestor').value = '';
        calendar.refetchEvents();
    });
});