"use strict";


const getSymptoms = () => {
    // Get the up to date food data from DB for the signed in user

    const formInputs = {'symptom_id': symptomID}; 

    $.get('/user_symptom_logs.json', formInputs, insertSymptomData);
};

const insertSymptomData = (res) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.

    const listOfSymptoms = res.symptom_experiences;
    const container = $('#symptom_logs');
    container.empty();
    container.append('<ul>')

    for (const currentSymptom of listOfSymptoms) {

        const momentTime = moment(currentSymptom.symptom_time)
        const adjustedTime = momentTime.tz('Etc/UTC')
        const symptom_time = moment(adjustedTime).format('dddd, MMMM Do YYYY @ h:mm a');

        container.append(`
            <li>
                ${symptom_time} <a href="/" id="symptom-${currentSymptom.id}">DELETE</a>
            </li>`
        );

        $(`#symptom-${currentSymptom.id}`).on('click', (evt) => {

            evt.preventDefault();

            const formInputs = {'symptom_log_id': currentSymptom.id} 

            $.post('/delete_symptom_log', formInputs, (res) => {
                window.location.href=`/symptom_view/${symptomID}`
              });
            });

        
    };
    container.append('</ul>')
}


// begin calendar
document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('weekly-calendar');


  $.get('/api/user_symptom_logs', (res) => {

    const symptomResults = res[symptomName]['results']; // 

  
    const calendar = new FullCalendar.Calendar(calendarEl, {
      // schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
      plugins: [ 'dayGrid', 'bootstrap' ],
      defaultView: 'dayGridWeek',
      height: 200,
      // events: res['heartburn']['results'],
      // eventColor: res['heartburn']['color'],
      themeSystem: 'bootstrap',
    });

    calendar.render();


      // symptom = string ('heartburn')
    for (const symptom_log of symptomResults) {
        // symptom_log_object = object
          const logEvent = {
            id: symptom_log['id'],
            title: symptom_log['title'],
            start: symptom_log['start'],
            color: res[symptomName]['color'],
          };

          calendar.addEvent(logEvent);
      }
    

    // first initialize the calendar, and then loop through the res symptoms to 
    // add to the color per symptom (with their respective colors!)

  })
});
// end calendar

getSymptoms();