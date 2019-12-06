"use strict";

document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');

  $.get('/api/user_symptom_logs', (res) => {

    const tooltipWrapper = info => {
      // console.log(info);
      $(info.el).tooltip({
            title: info.event.extendedProps.description,
            container: "body"
        });
    };

    const calendar = new FullCalendar.Calendar(calendarEl, {
      plugins: [ 'dayGrid', 'bootstrap', 'timeGrid'],
      themeSystem: 'bootstrap',
      defaultView: 'dayGridMonth',
      events: [],
      eventRender: tooltipWrapper,
      header: {
        left: 'dayGridMonth,timeGridWeek',
        center: 'title',
        right:  'today prev,next'
      }
    });

    calendar.render();

    for (const symptom in res) {

      // symptom = string ('heartburn')
      for (const symptom_log of res[symptom]['results']) {

        $.get(`/api/linked_ingredients/${symptom_log['title']}`, (result) => {
    
          const logEvent = {
                              id: symptom_log['id'],
                              title: symptom_log['title'],
                              start: symptom_log['start'],
                              color: res[symptom]['color'],
                              // description: 'hi hello'
                              description: result
          }
          calendar.addEvent(logEvent);
        });    
      }
    
    }
  });
});