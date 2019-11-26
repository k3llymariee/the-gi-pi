"use strict";

const getDailyFoodLogs = () => {
    // Get the up to date food data from DB for the signed in user
    ;debugger
    $.get(`/api/food_logs/${moment(selectedDate).format('YYYY-MM-DD')}`, insertFoodLogs);
}

const insertFoodLogs = (res) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.

    const listOfFoodLogs = res.food_logs;
    console.log(listOfFoodLogs)

    for (const currentFood of listOfFoodLogs) {

        const timeValue = moment(currentFood.ts)
        const adjustedTime = timeValue.tz('Etc/UTC').format('h:mm a')
        const container = $(`#${currentFood.meal}`)
        container.append(
            `<li> ${currentFood.food_name} @ ${adjustedTime}
                <a href="/food_log_view/${currentFood.id}">
                    <i class="fas fa-search"></i>
                </a>
                <a href="/food_log_view/${currentFood.id}" id="delete_${currentFood.id}">
                    <i class="fas fa-trash-alt"></i>
                </a>
            </li>`
        )
        
        $(`#delete_${currentFood.id}`).on('click', (evt) => {
        
            evt.preventDefault();

            if (confirm(`Delete ${currentFood.food_name} from ${currentFood.meal} at ${timeValue.tz('Etc/UTC').format('h:mm a')}`)) {

                const formInputs = {
                    'food_log_id': currentFood.id
                };

                $.post('/delete_food_log', formInputs, () => {
                    window.location = '/'
                });
            }
        })
    }
}

getDailyFoodLogs();