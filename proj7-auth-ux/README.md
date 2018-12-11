# Project 7: Adding authentication and user interface to brevet time calculator service

# contact and author
contact: bveber@uoregon.edu author: Brian Veber

# description
this project builds off of project 6 by adding password and token-based authentication for the brevet APIs. As a user you can register, login, and then use your token to access the APIs. Remember me, logout, and CSRF protection also available.

# how to run (also for grading)

    Note from project 6:
All APIs can be found on localhost port 5000. Individual API links (below) can be found via localhost:5001/.... The calculator used to submit, display, and calculate times can be found on localhost:5002.

To run, go to bash/terminal. cd proj7-auth-ux. cd DockerRestAPI. docker-compose build. docker-compose up. Visit your localhost at 5000,5001,5002 ports depending on what you are trying to do.

    Now in project 7:
Users can go to localhost/port 5001/ to visit the homepage, or index. On the index, users can choose to login, register, or logout. To run through all of the features, user should first register an account. Once that is done, then go to login. Logging in will give the user his/hers token (specifically after hitting submit on a successful login), which she/he should copy down in order to access the APIs. Now in order to visit the APIs, unlike project 6 you can't just use the links below. Use the links below, but at the end of them add: ?token="your token copied into here" without the quotations. For example: http://127.0.0.1:5001/listAll/json?token=eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0MzczNjk0MywiZXhwIjoxNTQzNzM3NTQzfQ.eyJpZCI6IjI2ODk0In0.c1X_AMV2bRhAka_fMmrtN_sG4uRg0UvXUP9v75giy9g would be an example of adding your token. Individual login and register links can be found by using your localhost:5001/api/login or api/register.


# project 6 recap to explain all features of brevet:

# Description
Recall the description of project 5:

This program, with the help of flask and ajax, calculates ACP controle times. It is an attempt to duplicate the calculator found at https://rusa.org/octime_acp.html. A full list of the rules can be found at https://rusa.org/pages/acp-brevet-control-times-calculator. However, here are some of the basic rules. The km you enter should not exceed your distance significantly. Open to close times on the first 0km will have 1 hour added. Km values cannot be negative. Values less than 20% of the original distance will be rounded down. Values less than the distance will be treated as normal.

Project 6 (this program) uses the same logic with the addition of REST APIs. You can view all APIs on port 5000 or visit individual APIs through port 5001. A list of APIs and their links and features can be found below under the "links program supports" header.

# How to run
All APIs can be found on localhost port 5000. Individual API links (below) can be found via localhost:5001/.... The calculator used to submit, display, and calculate times can be found on localhost:5002.

To run, go to bash/terminal. cd proj6-rest. cd DockerRestAPI. docker-compose build. docker-compose run. Visit your localhost at 5000,5001,5002 ports depending on what you are trying to do.

# Links this program supports:
* "http://<host:port>/listAll" should return all open and close times in the database
* "http://<host:port>/listOpenOnly" should return open times only
* "http://<host:port>/listCloseOnly" should return close times only

* "http://<host:port>/listAll/csv" should return all open and close times in CSV format
* "http://<host:port>/listOpenOnly/csv" should return open times only in CSV format
* "http://<host:port>/listCloseOnly/csv" should return close times only in CSV format

* "http://<host:port>/listAll/json" should return all open and close times in JSON format
* "http://<host:port>/listOpenOnly/json" should return open times only in JSON format
* "http://<host:port>/listCloseOnly/json" should return close times only in JSON format

* "http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format 
* "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
* "http://<host:port>/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
* "http://<host:port>/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format

