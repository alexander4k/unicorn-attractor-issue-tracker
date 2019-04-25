# Unicorn Attractor - Issue Tracker

A fully responsive web application for tracking issues of the Unicorn Attractor app.

Issues come in two varieties - bugs and features.

Users can create issue tickets to let developers know of any bugs they've come
across while using the Unicorn Attractor app or to share their suggestions on
features they'd like to see implemented in order to improve the app. 

To help developers get an idea of the number of occurances of each bug and of the
most sought after features, users have the ability to upvote and comment on issue tickets. 
The higher the number of upvotes a bug or a feature request has, the more its prioritized.

The aim is to spend 50% of development time fixing bugs and 50% implementing new features. 
Unfortunately, development time is expensive so in order to be able to achieve this aim,
upvoting feature requests costs money. Users can buy upvotes at the price of &euro;5 per upvote.
They can then upvote a feature request an unlimited amount of times as long as they posses upvotes.
On the other hand, upvoting a bug is free but a user can only upvote each bug once.
Payments are processed securely through Stripe and customer details are not saved anywhere.

Full transparency is offered to the users regarding the amount of work being done. 
Each issue has a progress status to let users know if the work on it has begun or if its been compeleted.
The home page contains charts showcasing the number of issues that have been completed the previous 7 days
and 12 months, the number of issues per status, as well as summaries of issues by popularity and date.

## UX

Inspired by [GitHub](https://github.com) and the [Stripe](https://stripe.com/en-IE/)
website, built using the [Bootstrap 4.3.1](https://getbootstrap.com/) framework. 

* On the homepage, a user is first presented with a login form and an option to register
  in order to allow them to contribute right away, as well as a link to view all current issues. 
  The homepage contains information about the Issue Tracker and how it works as well as a section
  to display various statistics regarding existing issues.
  Upon a successfull login, registration or log out, users are presented with a success message.

* The navigation bar contains links to pages where users can view all existing issues, only issues
  of type bug or only issues of type feature request. On each of the 3 pages, issues can be sorted
  by highest number of upvotes or comments through a dropdown menu. All 3 pages contain the button
  for creating an issue so that users don't have to waste time searching for it.

* The page for creating an issue is simple. A form with 3 fields.

* In list view, each issue occupies its own row so as not to have the content be too busy. The most
  relevant information about an issue is presented on the left side of the row, that being the type,
  status, title and date of creation while the right side contains information regarding the number
  of upvotes and comments, and the dates for last update or if completed, date of completion.

* In order to spare users having to scroll endlessly through a long list of issues, they are limited
  to 10 per page. Navigation links for navigation to previous/next pages only show once there is more
  issues than can fit on the page.

* Clicking on an issue's title will take the user to a page containing the details and comments of the
  issue. This is also the page where users can upvote the issue and post comments. Besides the
  information supplied on the previous list view of issues, this page contains description/content and
  the button used to delete an issue which only the author or the issue can see. Total number of comments
  display at one time is 10, after that users have to go to the next page of comments.

* Besides the links to issue pages, the navigation bar also contains links for a user's profile, home,
  login, logout and registration. The profile page displays information about the user, the number of
  upvotes they own and their profile picture, as well as buttons which allow for purchasing more upvotes
  or changing the profile picture. Every user has the default profile image starting off and in case
  there is no picture to display.

* When a user wants to purchase upvotes, they are taken to a page with a
  [Bootstrap Input Spinner](https://github.com/shaack/bootstrap-input-spinner) to select the amount of
  upvotes. The input spinner lets a user increase the number by holding down the button which is
  especially usefull on mobile devices.

* Once a user selects an amount of upvotes and click continue, they are taken to a page with feedback on
  their purchase and the card form to fill out in order to pay for the upvotes.

* When the purchase is complete, the user is presented with their new total amount of owned upvotes and
  a button to take them to the all issues page.

Mockups in a pdf format and user stories can be found here [UX assets](static)

During development, changes were made to the design and so the final version of the project differs somewhat from the mockups. 

## Features 

* User registration and authentication 
* Quick navigation options to issues grouped by their type
* Charts showing number of issues grouped by status, number of issues completed each day over the previous 7 days and
  each month over the previous 12 months
* Issues grouped and sorted to show most and least recent issues, and most popular bugs and features
* Ability to upvote issues
* Ability to comment on an issue
* E-commerce: Purchasing upvotes through Stripe
* Creation and deletion of issues
* Sorting of displayed issues by highest number of upvotes or comments
* User profiles and profile pictures which can be changed
* Pagination for list of issues and list of comments
 
## Technologies

* [Django](https://www.djangoproject.com/)
* [Python](https://www.python.org/)
* [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [JavaScript](https://www.javascript.com/)
* [JQuery](https://jquery.com/)
* [Bootstrap](https://github.com/shaack/bootstrap-input-spinner) and
  [Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)
  * Used for the layout of the page
* [Chart.js](https://www.chartjs.org/)
  * Used for charts
* [bootstrap-input-spinner](https://github.com/shaack/bootstrap-input-spinner)
  * Used for selecting number of upvotes
* [django-forms-bootstrap](https://github.com/pinax/django-forms-bootstrap)
  * Used for styling forms
* [Pillow](https://pillow.readthedocs.io/en/stable/)
  * Used for uploading images
* [django-storages](https://django-storages.readthedocs.io/en/1.7.1/backends/amazon-S3.html) and
  [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
  * Used for connecting with AWS S3 storage
* [Stripe](https://stripe.com/en-IE/)
  * Used for generating card details form and processing payments
* [Google Fonts Noto Sans](https://fonts.google.com/specimen/Noto+Sans)
  * Font
* [FontAwesome](https://fontawesome.com/)
  * Used for icons
* [dj-database-url](https://github.com/kennethreitz/dj-database-url)
  * Allows for utilizing the DATABASE_URL environment variable
* [gunicorn](https://gunicorn.org/)
  * Used for deploying app to Heroku
* [Markdown](https://en.wikipedia.org/wiki/Markdown)
  * Used for formatting README.md

## Testing [![Build Status](https://travis-ci.org/alexander4k/unicorn-attractor-issue-tracker.svg?branch=master)](https://travis-ci.org/alexander4k/unicorn-attractor-issue-tracker)
* To log in as superuser:
    * username - admin
    * password - 1234567a
### Manual Tests

1. **Index:**
   
    i. Attempt to log in with an unregistered username and password, verify that
    a message appears stating 'Username or password is incorrect'
    
    ii. Verify that all links to register redirect to the registration page

    iii. Verify "view issues" button redirects to all issues page
    
    iv. Attempt to log in with a registered username but wrong password, verify a
    message is displayed stating 'Username or password is incorrect'
    
    v. Attempt to log in with a registered username and correct password, verify
    page is refreshed, login form is no longer displayed login and register
    nagivation links were replaced by links to user profile and to log out. Verify
    a message appears stating "You have successfully logged in"
    
    vi. Verify when clicking on title of an issue, it redirects to that issues's
    details page
    
2. **Registration:**

    i. Attempt to register with a username already being used, verify a message
    is displayed stating 'A user with that username already exists.'
    
    ii. Attempt to register with an email already being used, verify a message
    is displayed stating 'Email address must be unique'
    
    iii. Attempt to register with a unique username and email but not matching
    password, verify a message is displayed stating 'Passwords must match'
    
    iv. Verify all fields are required
    
    v. Attempt to register with a unique username, email and matching passwords,
    verify being redirected to the index page where the login form has been
    replaced by a welcome message reflecting being registered
    
    vi. Attempt to access registration page, verify it redirects to index page
    
3. **All issues page:**

    i. Verify page contains issues of both types
    
    ii. Verify each issue has information regarding its type, status, title,
    author, date of creation and if completed, completion, and if updated,
    date of last update. Also the current number of upvotes and comments
    
    iii. Press the create issue button, verify it redirects to create issue
    page containing a form
    
    iv. Attempt to order issues on the page by "popular", verify issues are
    ordered by highest number of upvotes in descending format
    
    v. Attempt to order issues on the page by "comments", verify issues are
    ordered by highest number of comments in descending format
    
    vi. Attempt to click on an issue title, verify beind redirected to that
    issue's details page
    
    vii. If there are less than 10 issues, verify that the pagination links
    arent being displayed
    
    viii. Verify sorting condition is preserved when navigating to the next
    page of issues
    
3. **Bugs page:**
    
    i. Verify page contains only issues of type bug
    
    ii. Verify when sorting or paginating issues, bugs are the only type still
    being displayed
    
4. **Features page:**
    
    i. Verify page contains only issues of type feature request

    ii. Verify when sorting or paginating issues, feature requests are the only
    type still being displayed
    
5. **Create issue page:**

    i. Verify the page contains a form with 3 fields for title, type and description
    
    ii. Verify the title field and description are required in order to create an issue
    
    iii. Verify the issue type dropdown contains options for bug and feature
    
    iv. Attempt to create an issue, verify being redirected to the new issue's details page
    
6. **Issue details page:**

    i. Verify the page contains information regarding the issues's type, status, title,
    description, dates, number of upvotes and author. If being viewed by the author of the
    comment, it also contains a button next to the status element for deleting the issue. If
    logged in, below the issue details is a form for submitting a comment which includes a
    textarea field and a button to submit the comment, and if not logged in, the form is not
    displayed. If there are no comments for the issue, there is a message stating "There are
    no comments on this issue", if there are comments, each one occupies a single row and
    includes the user's that posted it profile image, name, date it was posted and the comment
    content.
    
    ii. Attempt to press the number of upvotes element to upvote the issue, verify being able
    to do so.
    
    - If the issue is of type bug and a user has upvoted it already, verify being unable to
    upvote it again
    
    - If the issue is of type feature and a user has no upvotes to spend, verify a message
    appears stating "You don't have upvotes to spend" and a user is unable to upvote it. If the
    user owns a number of upvotes, verify they can keep upvoting the issue as long as they have
    upvotes to spend.
      
    iii. As the author of the issue, attempt to press the delete button, verify being redirected
    to the all issues page where and that the issue no longer exists.
         
    iv. Attempt to submit a comment with no content, verify its required.
    
    v. Attempt to submit a comment, verify it appears at the start of the comments list.
    
    vi. Verify the comments list is sorted by newest comments descending
    
5. **Profile page:**

    i. Verify the user profile being displayed belongs to the logged in user
    
    ii. Verify the information displayed matches
    
    iii. Verify a newly registered user owns 0 upvotes and has the default image as
    their profile picture
    
    iv. Attempt to press the change profile image button, verify being redirected to
    a page where a user can upload a file to change their profile picture to
    
    v. Attempt to press the purchase upvotes button, verify being redirected to a page
    containing an input spinner user's can use to select the number of upvotes they
    want to buy
        
6. **Update profile image page:**

    i. Verify the page contains a file upload input and a button
    
    ii. Attempt to upload a file, verify being able to do it
    
    iii. Attempt to press the update image button, verify being redirected to the profile
    page and having the uploaded image as a profile image
    
7. **Being purchase page:**

    i. Verify page contins an input spinner for numbers and a button to continue the
    purchase
    
    ii. Attempt to increase the number by pressing the "+" button of the input spinner,
    verify it increases by 1
    
    iii. Attempt to hold down the "+" button of the input spinner, verify it keeps
    increasing the number
    
    iv. Attempt to press the continue with purchase button, verify being taken to a
    page containig a summary of the purchase, a form to enter your card details and
    a button to finish the purchase
        
8. **Continue purchase page:**
    
    i. Verify the page contains a summary of the purchase from the previous page, a
    form field to enter card details and a button to finalize the purchase

    ii. Verify the summary shows the number of upvotes being purchased, the amount a
    single upvote costs and the total price for the number of upvotes being purchased,
    e.g. If 7 upvotes are being purchased, the total price should be &euro;5.
        
    iii. Attempt to enter letters or special characters into the card field, verify
    being unable to do that
    
    iv. Attempt entering an incomplete card number into the card number field, verify
    a message pops up stating "Your card number is incomplete."
    
    v. Attempt to enter an invalid card number, verify a message appears stating
    "Your card number is invalid."
    
    vi. Attempt to enter a past year in the expiration date, verify a message appears
    stating "Your card's expiration year is in the past."
    
    vii. Attempt to enter an incomplete expiration date, verify a message appears
    stating "Your card's expiration date is incomplete."
    
    viii. Attempt to enter an incomplete security code, verify a message appears
    stating "Your card's security code is incomplete."
    
    ix. Attempt to enter an incomplete postal code, verify a message appears
    stating "Your postal code is incomplete."
    
    x. Attempt to finish the purchase with invalid card details, verify being unable
    to do so
    
    xi. Attempt to enter valid card details(4242 4242 4242 4242 04/24 242 24242),
    verify being redirected to a finished purchase page showing the new number of
    upvotes owned and a button link to the all issues page
    
9. **Finish purchase page:**

    i. Verify the page shows the correct number of upvotes owned by a user after
    purchasing them and a link to the all issues page
    
10. **Other:**

    i. When logging out, verify being taken to the homepage where a message appears
    stating "You have successfully logged out"
    
    ii. Regarding the statistics on the homepage:
      
     - Verify the "issues completed today" section contains the right date and only
     logs issues for that date
     
     - Verify the chart for "issues completed over the last 7 days" displays 7 days
     previous to the current day(if thursday, then wednesday, tuesday, monday, sunday,
     saturday, friday, thursday). Verify it logs the correct issues for those dates.
       
     - Verify the chart for "issues completed over the last 12 months" displays 12
     months previous to the current month(if april, then, march, february, january,
     december, november, october, september, august, july, june, may, april) verify
     it logs the correct issues for those dates.
       
    iii. Verify that the completed date of an issue is automatically set when
    changing the status of an issue to complete as admin
     
    iv. Verify the updated date of an issue is automatically updated when changing
    the status of an issue to anything or if a new comment has been submitted for
    that issue.
        
    v. Verify in case of status codes 400, 403, 404 and 500, users are redirected
    to the right custom error page.
    
    vi. Verify when a user is not logged in, the button for creating issues is
    replaced by links to register or login
    
    vii. Verify the brand image when clicked sends a user to the homepage
    
### Automated Tests

* For development, the default sqlit3 database is used, to run tests:
    * Run `python3 manage.py test` for all tests. To run tests only on specific
    apps, take a look at 
    [django's documentation](https://docs.djangoproject.com/en/2.2/topics/testing/overview/)
    * Or `pip3 install coverage` to install 
    [coverage.py](https://coverage.readthedocs.io/en/v4.5.x/)
        * then to run all tests `coverage run --source='.' manage.py test`
        * to run tests only on specific a app 
        `coverage run --source='.' manage.py test appname(e.g. accounts)`
        * run `coverage report` for an in-terminal report on results or 
        `coverage html` which will generate a new folder `htmlcov`. 
        * Inside the `htmlcov` folder locate `index.html` and run it.

* Other tests:
    * [W3C Markup Validation Service](https://validator.w3.org/)
      * Used for testing html
    * [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
      * Used for testing css
    * [Mobile Friendly Test](https://search.google.com/test/mobile-friendly)
      * Used for testing mobile layout

## Deployment 

Deployed on Heroku - [Issue Tracker](https://unicorn-attractor-issue-tracker-alexander4k.c9users.io/).

* To run locally:
    * Clone the repository by copying the clone url
    * Run `git clone` followed by the copied url
    * `cd` into `unicorn-attractor-issue-tracker`
    * Run `pip3 install -r requirements.txt` to install all the dependencies 
    * Use the `env.example` file to set environemt virables
    * Run `python manage.py makemigrations` to make migrations
    * Run `python manage.py migrate` to migrate
    * Create a new superuser `python3 manage.py createsuperuser`
    * Run `python manage.py collectstatic` to collect static files
    * Run  `python3 (path to manage.py file) runserver $IP:$PORT`
* To deploy to heroku:
    * `git init` to create a new repository
    * `git add .`
    * `git commit -m "Initial commit"`
    * Create Procfile in your top directory and in it add 
    `web: gunicorn issuetracker.wsgi:application`
    * Push to GitHub new repository
    * Create a new Heroku app
    * In Resources tab, provision Heroku Postgres
    * In Deployment tab, select GitHub as deployment method then find and
    connect your repository
    * In Settings tab, add all the environment variables to Config vars and
    `DISABLE_COLLECTSTATIC=1`
    * Go back to Deployment tab and in Manual deploy deploy branch
    * Open the app

## Credits

* Brand image - [Icons8](https://icons8.com/icons/set/unicorn)
* Default profile image - 
[Pixabay](https://pixabay.com/vectors/blank-profile-picture-mystery-man-973460/)

## License

MIT
