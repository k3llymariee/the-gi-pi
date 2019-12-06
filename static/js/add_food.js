"use strict";

const getFoodData = () => {
    // Get the up to date food data from DB for the signed in user

    $.get('/user_foods.json', (res) => insertFoodData(res, $('#display-db-search')));
}

const insertFoodData = (res, container) => {
    // Once the data has been provided by the server,
    // insert it into the page as an HTML string.

    const listOfFoods = res.foods;
    container.empty();

    if (listOfFoods.length === 0) {
        container.append(`<br><i>No foods found</i> 😢  
                                <a href='/manual_add'>add it manually</a>`);
    }

    else {
        for (const currentFood of listOfFoods) {
        // consider adding each food as an option and allow them to add with timestamp to food log here

            container.append(`
            <div class="row">
                <div class="col-2 add-foods">
                    <button type="button" class="btn btn-primary addFood" data-toggle="modal" data-target="#addFoodModal" data-name="${currentFood.food_name}" data-id="${currentFood.id}"><i class="fas fa-plus"></i></button>
                    <div class="modal fade" id="addFoodModal" tabindex="-1" role="dialog" aria-labelledby="addFoodModalLabel" aria-hidden="true">
                      <div class="modal-dialog" role="document">
                        <form action="/add_food" method="POST">
                            <div class="modal-content">
                              <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalLabel" style="color: #032059">Add food</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                  <span aria-hidden="true">&times;</span>
                                </button>
                              </div>
                              <div class="modal-body" style="color: #032059">
                              <h4 class="food-name"></h4>
                                  <div class="form-group">
                                    <label for="time_eaten">What time did you eat this?</label>
                                    <input type="datetime-local" class="form-control" name="time_eaten" id="time_eaten">
                                  </div>
                                  <div class="form-group">
                                    <label for="meal_to_add">For which meal?</label>
                                        <select class="custom-select" id="meal_to_add" name="meal_to_add">
                                            <option value="1">Breakfast</option>
                                            <option value="2">Lunch</option>
                                            <option value="3">Dinner</option>
                                            <option value="4">Snacks</option>
                                        </select>
                                  </div>
                                  <input type="hidden" name="food_id" id="food_id" /><br> 
                                </form>
                              </div>
                              <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary">Add!</button>
                              </div>
                            </div>
                        </form>
                      </div>
                    </div>
                </div>
                <div class="col-7 justify-content-center align-self-center">
                    ${currentFood.food_name} (${currentFood.brand}) 
                </div>
            </div>`
            );

            const updateMeal = () => {

                const dateInput = new Date($('#time_eaten').val());

                // if timeEaten is between 6am and 9am -> value of meal = breakfast
                // if timeEaten is between 11:00am and 1:30 pm -> valeu of meal = lunch
                // if timeEaten is between 5:30pm and 9:00pm -> value of meal = dinner
                // ELSE value of meal = snack

                if (dateInput.getHours() > 6 && dateInput.getHours() < 9) {
                    $('#meal_to_add').val('1');  // breakfast
                } else if (dateInput.getHours() > 11 && dateInput.getHours() < 14) {
                    $('#meal_to_add').val('2');  // lunch
                } else if (dateInput.getHours() > 17 && dateInput.getHours() < 21) {
                    $('#meal_to_add').val('3'); // dinner
                } else {
                    $('#meal_to_add').val('4');  // snacks
                }
            };

            const pad = (n) => {
                if (n < 10) {
                    return '0' + n
                } else {
                    return n
                }
            };

            const defaultTime = () => {

                const currentDate = new Date()
                const date = currentDate.getDate();
                const month = currentDate.getMonth() + 1;  //January is 0 not 1
                const year = currentDate.getFullYear();
                const hours = currentDate.getHours();
                const minutes = currentDate.getMinutes();

                // The format is "yyyy-MM-ddThh:mm"

                const currentDateTime  = pad(year) + "-" + pad(month) + "-" + pad(date)
                    + "T" + pad(hours) + ":" + pad(minutes);

                $('#time_eaten').val(currentDateTime)

                updateMeal();
            }

            defaultTime();

            $('#time_eaten').on('change', updateMeal)

            $(function () {
                $('[data-toggle="tooltip"]').tooltip()
            })

            $('#addFoodModal').on('show.bs.modal', function (event) {
                const button = $(event.relatedTarget) // Button that triggered the modal
                const food_id = button.data('id') // Extract info from data-* attributes
                const food_name = button.data('name') // Extract info from data-* attributes
                // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
                // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
                const modal = $(this)
                modal.find('#food_id').val(food_id)
                modal.find('.modal-title').text('Add ' + food_name)
            })
        };
    }
}





$('#search-food').on('submit', (evt) => {
    evt.preventDefault();

    const searchTerm = $('#search_term').val();

    $.get(`/food_search/${searchTerm}`, (res) => {
        
        const foods = res["foods"]
        const container = $('#display-search');
        const manualAdd = $('#manual_add')
        manualAdd.empty()
        container.empty()

        if (foods.length === 0) {
            manualAdd.append(`<br><br><p>
                                No results found 😢  
                                <a href='/manual_add'>add it manually</a>
                            </p>`)
        }

        else {
            manualAdd.append(`<div><br><p>
                                Still can't find what you're looking for? 
                                <a href='/manual_add'>Add it manually</a>
                            </p>
                            <p>
                                <cite>Search results powered by &nbsp;
                                    <a href="http://www.nutritionix.com/api" target="_blank">
                                        Nutritionix API
                                    </a>
                                </cite>
                            </p></div>`)
        

            for (const food of foods) {

                container.append(`
                    <div class="col-3 mb-4">
                        <div class="card">
                            <img src="${food.photo.thumb}" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title">${food.brand_name_item_name}</h5>
                                <p class="card-text">(${food.brand_name})</p>
                                <a href="nutrionix_check/${food.nix_item_id}"
                                    id="${food.nix_item_id}" class="btn btn-primary">Add food</a>
                            </div>
                        </div>
                    </div>
                    `);

                $(`#${food.nix_item_id}`).on('click', (evt) => {

                    evt.preventDefault();

                  $.get(`/nutrionix_check/${food.nix_item_id}`, (res) => {
                    if(confirm(res['text'] + res['food_name'] + '\n\n Ingredients:' + res['ingredients']))
                        window.location.href=`/nutrionix/${food.nix_item_id}`
                  });
                });   
            };
            // container.append('Powered by &nbsp;<a href="http://www.nutritionix.com/api" target="_blank">Nutritionix API</a>')
        }
    });
  });

$('#db-search').on('submit', (evt) => {
    evt.preventDefault();

    const dbSearchTerm = $('#db_search_term').val();

    $.get(`/db_food_search/${dbSearchTerm}`, (res) => insertFoodData(res, $('#display-db-search-specific')));
});

// Get intial user foods when page initially loads!
getFoodData();

