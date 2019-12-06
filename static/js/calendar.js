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
      plugins: [ 'dayGrid', 'bootstrap' ],
      themeSystem: 'bootstrap',
      events: [],
      eventRender: tooltipWrapper,
    });

    calendar.render();

    for (const symptom in res) {
      // symptom = string ('heartburn')
      for (const symptom_log of res[symptom]['results']) {
        // symptom_log_object = object
          const logEvent = {
            id: symptom_log['id'],
            title: symptom_log['title'],
            start: symptom_log['start'],
            color: res[symptom]['color'],
            description: 
              $.get(`/api/linked_ingredients/${symptom}`, (res) => {
                console.log('RESRES:', res)
                // ;debugger
                console.log('typof', typeof(res))
                return(res)
              }) ;debugger
          };

          calendar.addEvent(logEvent);
      }
    
    }

    // first initialize the calendar, and then loop through the res symptoms to 
    // add to the color per symptom (with their respective colors!)

  })
});