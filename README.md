# Trello

This app is to provide the restful services for Task management system similar to Trello.
User should be able to perform the following tasks for which there are API's written:

#Setup

1. Git clone the repository.
2. Delete the venv folder and install your own virtual environment using pip install virtualenv > virtualenv venv
3. Activate the virtual environment before installing requirements "source venv/bin/activate"
3. pip install -r requirements.txt will install all the necessary requirements.
4. Go to the trello > taskmanager folder and run the command "python manage.py runserver 0.0.0.0:port" port is optional.
5. If port is not mentioned the default port is 8000.
6. Now you will be able to access the API endpoint URL's


#API's that can be used:

We are assuming that you are running the application on default 8000 port

List/Create Teams: http://localhost:8000/trello/teams/
List User Specific Teams: http://localhost:8000/trello/user/teams/ (User authentication is required for this to display)
List/Edit/Delete Specific Team: http://localhost:8000/trello/team/1/

List/Create Boards: http://localhost:8000/trello/boards/
List Team Specific Boards: http://localhost:8000/trello/boards/team/1 (Team ID should be passed in the URL)
List/Edit/Delete Specific Board: http://localhost:8000/trello/board/1/

List/Create Lists: http://localhost:8000/trello/lists/
List All the Lists of a specific Board: http://localhost:8000/trello/lists/board/1 (Board ID should be passed in URL)
List/Edit/Delete Specific List: http://localhost:8000/trello/list/1/

List/Create Cards: http://localhost:8000/trello/cards/
List all the cards specific to a List: http://localhost:8000/trello/cards/list/1 (List ID should be passed in URL)
List/Edit/Delete Specific Card: http://localhost:8000/trello/card/1/

#Current Features:

1. User Signup Implemented.
2. User login implemented.
3. User home screen dashboard displays all the teams he belongs to (List User Specific Teams)
4. User can delete the team.

#Technologies:

Django 1.11.16
Django Rest Framework
BULMA Flexbox Framework for styling
Vue.js
Axios
