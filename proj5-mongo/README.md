# contact and author

contact: bveber@uoregon.edu
author: Brian Veber

# Proj5-mongo

This project extends proj4-brevets by adding display and submit keys. The submitkey will store all the values inputted by the user including km, open, and close time. Using the display button will show you all of the values that you have submitted.

#Description

Description: This program, with the help of flask and ajax, calculates ACP controle times. It is an attempt to duplicate the calculator found at https://rusa.org/octime_acp.html. A full list of the rules can be found at https://rusa.org/pages/acp-brevet-control-times-calculator. However, here are some of the basic rules. The km you enter should not exceed your distance significantly. Open to close times on the first 0km will have 1 hour added. Km values cannot be negative. Values less than 20% of the original distance will be rounded down. Values less than the distance will be treated as normal. 

#How to run

cd to dockerMongo and run docker-compose up in bash. Then visit your localhost.
