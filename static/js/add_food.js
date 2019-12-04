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
    container.append('<ul>')

    for (const currentFood of listOfFoods) {

        // consider adding each food as an option and allow them to add with timestamp to food log here
        container.append(`
            <li>
                ${currentFood.name} (${currentFood.brand}) 
                <a href="/add_food/${currentFood.id}">
                    <i class="fas fa-plus"></i>
                </a>
            </li>`
        );
    };
    container.append('</ul>')
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
        manualAdd.append(`<br><br><p>
                            Still can't find what you're looking for? 
                            <a href='/manual_add'>Add it manually</a>
                        </p>`)

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
        container.append('</div>')
    });
  });

$('#db-search').on('submit', (evt) => {
    evt.preventDefault();

    const dbSearchTerm = $('#db_search_term').val();

    $.get(`/db_food_search/${dbSearchTerm}`, (res) => {
        
        const foods = res["foods"]
        const container = $('#display-db-search-specific');
        container.empty()
        $('#empty-db').empty()

        if (foods.length === 0) {
            container.append('<br><i>No foods found</i>');
        }

        else {

            container.append("<ul>");

            for (const food of foods) {
                container.append(`<div>
                    <li>${food.food} (${food.brand})
                        <a href="/add_food/${food.id}">
                            <i class="fas fa-plus"></i>
                        </a>
                    </li></div>`
                );

            container.append('</ul');
            };
        }
    });
});

// Get intial user foods when page initially loads!
getFoodData();