# 🕵️‍♀️ The G.I. P.I.

## Summary

**The G.I. P.I.** (or Gastrointestinal Private Investigator) is a webapp that allows users to enter in their foods and health symptoms, and tracks individual ingredients that might be the cause of those symptoms. 

Users have the ability to find and create new foods to add to their diaries based on the time and date they consumed them, and track any health symptoms they might have by date, time, and severity. 

## Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [About Me](#aboutme)

## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: [Nutritionix API](https://www.nutritionix.com/business/api)<br/>
Libraries: [FullCalendar.io](https://fullcalendar.io/)

The G.I. P.I. is built on a Flask server with a PostgreSQL database, utilizing SQLAlchemy as the ORM. The frontend templating uses Jinja2, the HTML incorporates Bootstrap, and the Javascript files use JQuery + AJAX to interact with the backend. The calendars are rendered using FullCalendar. A handful of server routes are tested using the Python unittest module.

## <a name="features"></a>Features

### Logging In

![Login Redirect](/the-gi-pi/static/img/_readme-img/new_user.gif)

Only logged in users have access to the feature in the site - attempting to go to the homepage will redirect to the register/log in page with a flash warning. 

Once a user is logged in, they will see a daily view of their food and symptom logs. This is done through a combination of Jinja and AJAX requests to my PostgreSQL database. 

The main actions a user can take are on this page - adding a food and adding a symptom. 

### Clicking “Add Food!” 
This takes the user to a separate page that allows users to add a food to their log in one of four ways (the fourth is hidden!).

1. Search Our database is an AJAX get request to the database for all foods that have been added by all users of the application.

2.  Add a food from your history is an AJAX request to the database for the foods that have been added by this specific user, in order of what had been recently added.

* Within this modal, when the time of the meal is entered the app will guess which meal it is based on that time, though of course you can change this if decide that 12pm cookie was only a snack!  

3. Add a food from an external database, which is an AJAX request to a third party API called Nutritionix that provides information about branded food items.

4. If all else fails, a food can also be entered in manually. 
* This form accepts a comma separated list of ingredients, which will be cleaned up and parsed into individual ingredients (with a server-side check to ensure that no duplicate ingredients are added).  
* Each method of adding a new food adds a food log event to by database through SQLalchemy. 

### Clicking “Add Symptom!” 
This presents the user with a Bootstrap modal the enter in the symptom they’ve experienced, the time at which they felt it, and a ranking of its severity. The value for the time they experienced is defaulted to the current time using a javascript function, though the user can adjust as needed. The severity was a data point that I added after my MVP, as eventually I would like to have some kind of a data visualization of the relationships I’ve created in my database. 

### Viewing a Symptom
By viewing a symptom, users are presented with the history of their symptom experiences, as well as the ingredients that the system has identified as common occurrences. This is accomplished through a DB query that uses a window of time as a lookback period to first find the foods that were consumed within that window, and then their ingredients to find the number of times those ingredients appeared. 

### Flagged Ingredients
Currently, users need to manually flag ingredients as a cause of the symptoms when the trends are shown to them. Doing so will take them to a holistic view of all their symptom occurrences. Hovering over each symptom displays a javascript tooltip that shows the symptoms they’ve flagged. 

### Viewing All Symptoms
Clicking 'My Symptoms' takes the user to a calendar view, which shows all symptom events recently experienced by the user. This is done through an AJAX request to the server, and populated within a calendar implemented using the FullCalender javascript library. 

## <a name="install"></a>Installation

Coming soon! I do have a requirements.txt though :)

## <a name="aboutme"></a>About Me

I began my career at one of the Big Four Accounting Firms. My main focus was on startups in the payment processing space, with main clients like Square & Stripe. Determined to keep helping smaller companies but provide more value to them, I got a job as a Revenue Accountant at Slack in 2015. While there, I started taking on the responsibilities of a Product Manager during the company's transition of ERP systems, and formally moved into Product Management in a 6-month rotation. During my rotation I worked even more closely with engineers, de-bugging and writing pseudocode to help solve difficult payment problems. At the end of the rotation, I decided to make the full jump into software development and joined Hackbright's December 2019 cohort!