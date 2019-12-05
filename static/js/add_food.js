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
        container.append('<br><i>No foods found</i>');
    }

    else {
        for (const currentFood of listOfFoods) {
        // consider adding each food as an option and allow them to add with timestamp to food log here

            container.append(`
            <div class="row">
                <div class="col-1 add-foods">
                    <a href="/add_food/${currentFood.id}" data-toggle="tooltip" data-placement="left" title="Add this food">
                        <i class="fas fa-plus"></i>
                    </a>
                </div>
                <div class="col-5 align-self-start">
                    ${currentFood.food_name} (${currentFood.brand}) 
                </div>
            </div>`
            );

            $(function () {
                $('[data-toggle="tooltip"]').tooltip()
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
                    <div class="col mb-4">
                        <div class="card" style="width: 18rem;">
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
            container.append('Powered by &nbsp;<a href="http://www.nutritionix.com/api" target="_blank">Nutritionix API</a>')
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

