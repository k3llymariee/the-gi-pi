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

getSymptoms();