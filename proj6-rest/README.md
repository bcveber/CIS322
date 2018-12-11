# contact and author
contact: bveber@uoregon.edu author: Brian Veber

# Project 6: Brevet time calculator service
This project expands project 5 and creates REST APIs for the user to choose from.

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