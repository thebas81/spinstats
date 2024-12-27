# SPINSTATS
#### Video Demo:  https://youtu.be/kOJl1D7dtoE
#### Description:
Spinstats is web application built in Flask where a cyclist can record rides and consult training history, complete with weekly, monthly, yearly and all-time stats.\
With this app it's also possible to track the progress to reach big milestones, like riding all around the world or climbing mount Everest!

# My work
I deepened my knowledge of Flask, including some best practices, such as managing routes and models in separate files.  
For interfacing with the SQLite database, I used the `Flask_SQLAlchemy` package, leveraging the ability to define models for creating (and subsequently using) the data structures required for the app's functionality.  
I utilized an `__init__.py` file to include the app's basic configurations, which then calls the two files responsible for managing routes and models.  
I also used a separate `helpers.py` file where I added utility functions, such as a function to ensure the user is logged in (redirecting to the login page if not), or data validation functions for input during the creation of a new ride.  
User session management is handled by `Flask-Session` package.  
I explored the use and management of dates in Flask with the `datetime` module and how dates are handled with `Flask SQLAlchemy`, including querying data within specific time windows (week, month, year).  
I used the Bootstrap CSS framework, taking advantage of tables, typography, forms, and components such as progress bars, buttons, alerts (for error messages), and the navbar.  
Throughout the project, I used GIT for version control and file management.

# App Usage Guide  
## User Registration  
You can register your username via the "Register" menu. This will open the user registration page where you can enter the required information to create an account. If the provided data is incorrect or incomplete, the system will prompt you to re-enter the details.  

## Login  
Once your account is registered, you will be redirected to the login page, where you can log in using your username and password.  

## Dashboard  
After logging in, you will be redirected to your Dashboard, which provides a complete overview of your training sessions.  
On this page, you'll find a list of all your recorded rides, as well as weekly, monthly, yearly, and all-time training statistics (from the date you registered on the site).  

### Rides  
On the left side of the Dashboard, there is a table displaying the last 10 rides entered by the user. From here, you can also add a new ride by clicking the corresponding button (or via the menu in the navigation bar).  
The rides you've added can be edited or deleted by clicking the respective "Update" or "Delete" buttons. Clicking "Delete" will display a confirmation prompt to delete the record.  
On the other hand, clicking "Update" will open the ride update page, where you can modify the previously entered data.  

### Stats  
On the right side of the Dashboard, you can find weekly, monthly, yearly, and all-time training statistics.  

### Milestones  
At the bottom of the Dashboard, you'll see two major milestones, displayed with convenient progress bars that show the percentage of progress toward these goals: "Around the World" and "Climbing Mount Everest."  

## Account  
Using the navigation bar, you can select "Account" to open the account update page. You will not be able to update your "username" or "email" as these are unique values in the database.  

## Logout  
Finally, by clicking the Logout button, your session will end, and you will be redirected to the app's home page.  

### Thank you!