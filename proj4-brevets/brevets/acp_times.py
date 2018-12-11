"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

#tables with locations and their min/max speeds
minSpeedT = {200:15.0, 300:15.0, 400:15.0, 600:11.428, 1000:13.333}
maxSpeedT = {200:34.0, 300:32.0, 400:30.0, 600:28.0, 1000:26.0}

#only the max and min speeds, no keys like above
#shown in descending order
minSpeedOnly = [15.0, 15.0, 15.0, 11.428, 13.333]
maxSpeedOnly = [34.0, 32.0, 30.0, 28.0, 26.0]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    #This is to account for when the route leaks over slightly,
    #like in example 1 where they take 205 back down to 200
    #will set the route back to the next highest interval and
    #5 or whatever number won't be counted
    if (brevet_dist_km < control_dist_km):
        control_dist_km = brevet_dist_km

    #we are now going to get the time for the route with our corr.
    #max values
    rawTime = timeCalculator(control_dist_km, maxSpeedOnly)

    #once we know how much time the route took, simply add it to the
    #initial time and we are good to go
    finalTime = timeAdder(rawTime, brevet_start_time)
    return finalTime

#adds time traveled to initial time we had
def timeAdder(rawTime, initialTime):

    #multiply by 60 to get into minutes. Then adding .5 will ensure that
    #any left over gets rounded, as changing it to an int with the command
    #below will take care of any decimal still there
    #**testing appeared to make the .5 necessary to round up and get values
    #more in line with the actual calculator
    totMinutes = ((rawTime * 60) + .5)
    int(totMinutes)

    #use our arrow functions to add the minutes from timeCalculator() and
    #translate that into a formatted time
    finalTime = arrow.get(initialTime).shift(minutes=+totMinutes).isoformat()

    return finalTime

#calculates the km traveled into the form of time
def timeCalculator(kmGiven, speedTable):
#to help visualize:
#minSpeedOnly = [15.0, 15.0, 15.0, 11.428, 13.333]
#maxSpeedOnly = [34.0, 32.0, 30.0, 28.0, 26.0]

    #keeps on chopping off 200 and going down the speeds
    #initializers
    x = 0
    totTime = 0

    #There are intervals of 200. So essentially what this function
    #does is cycle through these intervals. So long as its greater than
    #200 (which signifies a new interval) we will keep cycling through the
    #main part of the min/max speed values. We also have x < 3 b/c we don't
    #want it to somehow run more than 4 times inside the loop (as the last
    #line before the return statement is the 5th, if any, pass through). This
    #is b/c our min/max only have 5 speed intervals each.
    #It will keep going deeper into min/maxSpeedOnly until it runs out from
    #being chopped off by 200 for each interval pass.
    while kmGiven > 200:
        if x < 3:
            totTime = totTime + (200/speedTable[x])
            x += 1
            kmGiven = kmGiven - 200

    #4th pass right here or 1st if less than 200
    #this will be 200 or the remainder (something less than 200) for
    #the final interval pass to evaluate
    totTime = totTime + (kmGiven/speedTable[x])

    return totTime
  

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    #this is to account for the 0 value starting point where the original
    #calculator webpage adds an hour on for this part, so follow suit here
    if control_dist_km == 0:
        finalTime = timeAdder(1, brevet_start_time)
        return finalTime

    else:
    
        #very similar to open_time. Calculate the time w/ the intervals,
        #then add it to the initial time and return
        rawTime = timeCalculator(control_dist_km, minSpeedOnly)
        finalTime = timeAdder((rawTime), brevet_start_time)
        return finalTime

