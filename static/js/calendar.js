"use strict";


document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');


  $.get('/api/user_symptom_logs', (res) => {

    console.log(res)


  
    const calendar = new FullCalendar.Calendar(calendarEl, {
      // schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
      plugins: [ 'dayGrid', 'bootstrap' ],
      // defaultView: 'dayGridWeek',
      // height: 200,
      // events: res['heartburn']['results'],
      // eventColor: res['heartburn']['color'],
      themeSystem: 'bootstrap',
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
          };

          calendar.addEvent(logEvent);
      }
    }

    // first initialize the calendar, and then loop through the res symptoms to 
    // add to the color per symptom (with their respective colors!)

  })
});