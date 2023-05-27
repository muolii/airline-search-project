# Jenny You
# Programming Project - Airline Program
# Due: May 3nd 2023

# Cheks if user enters a valid file name and attempts to open the data file
def openFile():
    # Sets initial value to False
    goodFile = False
    while goodFile == False:
        # Tries to open the file using name given
        fname = input("Please enter a file name:")
        try:
            # If the name is valid, goodFile is True and the loop is exited
            dataFile = open(fname,'r')
            goodFile = True
        # If an IOError exception is raised, user is prompted to try again
        except IOError:
            print("Invalid file name try again...")
    return dataFile

# Opens a data file and appends all data into specific lists
def getData():
    dataFile = openFile()
    line = dataFile.readline()
    line = line.strip()
    airlineList = []
    numList = []
    departList = []
    arriveList = []
    costList = []
    while line != '':
        airline, num, depart, arrive, cost = line.split(',')
        airlineList.append(airline)
        numList.append(int(num))
        departList.append(depart)
        arriveList.append(arrive)
        costList.append(int(cost.replace("$","")))
        line = dataFile.readline()
        line = line.strip()
    return airlineList, numList, departList, arriveList, costList

# Ensures input airline is valid
def airValid(airlineList):
    OK = False
    while OK == False:
        airline = input("Enter airline name:")
        if airline in airlineList:
            OK = True
        else:
            print("Invalid input -- try again")
    return airline

# Ensures flight number is valid
def numValid(numList):
    num_OK = False
    while num_OK == False:
        try:
            flightNumber = int(input("Enter flight number:"))
            if flightNumber in numList:
                num_OK = True
        except ValueError:
                print("Invalid input -- try again")
    return flightNumber

# Searches index of flight info in lists and returns index
# Prints results in main using index
def findFlight(airlineList, numList):
    # Ensures airline is a proper value
    airline = airValid(airlineList)
            
    # Ensures flight number is valid 
    flightNumber = numValid(numList)
        # Returns index of selected flight 
    for i in range(len(airlineList)):
        if airlineList[i] == airline and numList[i] == flightNumber:
            return i
    return -1

def validDuration():
    OK = False
    while OK == False:
        try:
            max_duration = int(input("Enter maximum duration (in minutes):"))
            OK = True
        except ValueError:
            print("Entry must be a number")
    return max_duration

# Searches through all flights until finding one with the shortest duration
# Obtains index, and prints results in main function
def shorterFlights(departList, arriveList):
    indexList = []
    max_duration = validDuration()
    # Converts departure and arrival at index to duration
    for i in range(len(departList)):
        # Replaces : with . in order to do math
        arrival = timeConvert(arriveList[i])
        departure = timeConvert(departList[i])
        # Multiplies result by 60 to get minutes
        duration = arrival - departure
        # Appends to list if less than max
        if duration <= max_duration:
            indexList.append(i)
    
    return indexList

# Searches through all flights for the cheapest from given airline
# Prints results in main
def cheapestFlight(airlineList, costList):
    lowest_cost = costList[0]
    lowest_index = 0
    # Ensures airline input is valid
    airline = airValid(airlineList)
    # Iterates through length of airlineList until given airline is found:
    for i in range(len(airlineList)):
        # Checks if airline is the one you are searching for 
        if airlineList[i] == airline:
                # If lower cost is found, set new lowest and take index
                if costList[i] < lowest_cost:
                    lowest_cost = costList[i]
                    lowest_index = i
    return lowest_index

# Searches through all flights to find a list of flights that depart after a specified time
# Prints results in the main function
def departFlght(departList):
    indexList = []
    time = timeValid()
    # Converts time to decimal in order to see what flights occur after         
    time = timeConvert(time)
    for i in range(len(departList)):
        if timeConvert(departList[i]) > time:
            # Append index into list
            indexList.append(i)
    return indexList

# Converts time into minutes
def timeConvert(time):
    total_minutes = 0
    hours, minutes = time.split(":")
    total_minutes += int(hours) * 60
    total_minutes += int(minutes)
    return total_minutes
    

# Ensures user enters a valid time
def timeValid():
    time = input("Enter earliest departure time: ")
    OK = False
    while OK == False:
        try:
            hours, minutes = time.split(":")
            # Checks if time follows proper format, where hours and minutes must be of length 2
            if len(hours) == 2 and len(minutes) == 2 and 0 <= int(hours) <= 24 and 0 <= int(minutes) <= 60:
                OK = True
            else:
                time = input("Invalid time - Try again ")
        except ValueError:
            time = input("Invalid time - Try again ")
    return time

# Obtains average price of all available flights
def averageCost(costList):
    average = 0
    # Iterates through length of costList:\
    for i in range(len(costList)):
        # Adds each item in costList to sum after removing dollar sign
        average += costList[i]
    # Calculates average by dividing sum by length of costList
    average = round((average / len(costList)), 2)
    return average

# Sorts all flights by departure and writes data to new file
# Simultaneously sorts all lists
def timeSorted(departList):
    newList = departList.copy()
    # Creates list of indeces from range 0 to length of list
    indexList = list(range(0, len(newList)))
    # Iterates through length of departure list:
    for i in range(0, len(newList)):
        # Sets min to i
        min = i
        for j in range(i+1, len(newList)):
            # Converts time to int and then compares:
            if timeConvert(newList[j]) < timeConvert(newList[min]):
                # Sets min value to j
                min = j
        # Swaps item at index i and item at index max in list of indeces
        newList[i], newList[min] = newList[min], newList[i]        
        indexList[i], indexList[min] = indexList[min], indexList[i]
    return indexList

# Writes data into new file
def sortedFile(indexList, airlineList, numList, departList, arriveList, costList):
    outName = "time-sorted-flights.csv"
    outFile = open(outName, "w")
    for i in range(len(indexList)):
        outFile.write(airlineList[indexList[i]] + ',' + str(numList[indexList[i]]) + ',' + departList[indexList[i]] + ',' +  arriveList[indexList[i]] + ',' + "$" + str(costList[indexList[i]]) + "\n")
    outFile.close()
    print("Sorted data has been written to file: ", outName)
    return

# Makes sure user enters a value that is within the options available  
def validChoice():
    OK = False
    while OK == False:
        try:
            choice = int(input("Choice ==> "))
            if choice < 1 or choice > 7:
                print("Entry must be between 1 and 7")
                OK = False
            else:
                OK = True
        except ValueError:
            print("Entry must be a number")
    return choice

# Displays menu choices for user and ensures user enters valid choice
def getChoice():
    # Displays menu choices
    print("")
    print("Please choose one of the following options:")
    print("1 -- Find flight information by airline and flight number")
    print("2 -- Find flights shorter than a specified duration ")
    print("3 -- Find the cheapest flight by a given airline")
    print("4 -- Find flight departing after a specified time")
    print("5 -- Find the average price of all flights")
    print("6 -- Write a file with flights sorted by departure time")
    print("7 -- Quit")
    
    # Makes sure user enters a value that is within the options available  
    choice = validChoice()
            
    print("")       
    return choice

# Prints results into neat display
def printResults(index, airlineList, numList, departList, arriveList, costList):
    print("The flight that meets your criteria is:")
    print("")
    # Adds dollar sign back to cost:
    cost = "$" + str(costList[index])
    # Formats data into table where contents are equally spaced
    print("{:<10s}{:>4s}{:>10s}{:>10s}{:>10s}".format("AIRLINE","FLT#","DEPART","ARRIVE","PRICE"))
    print("{:<10s}{:>4s}{:>10s}{:>10s}{:>10s}".format(airlineList[index],str(numList[index]), departList[index], arriveList[index], cost))
    return

# Seperate print function for if there are multiple results
def printResultsList(indexList, airlineList, numList, departList, arriveList, costList):
    if indexList == []:
        print("")
        print("No flights meet your criteria")
    else:
        print("The flights that meet your criteria are:")
        print("")
        # Uses string format allign in order to format the string
        # https://docs.python.org/2.7/library/string.html#format-specification-mini-language
        print("{:<10s}{:>4s}{:>10s}{:>10s}{:>10s}".format("AIRLINE","FLT#","DEPART","ARRIVE","PRICE"))
        for i in range(len(indexList)):
            cost = "$" + str(costList[indexList[i]])
            print("{:<10s}{:>4s}{:>10s}{:>10s}{:>10s}".format(airlineList[indexList[i]],str(numList[indexList[i]]), departList[indexList[i]], arriveList[indexList[i]],cost))
    return

# Main function
def main():
    # Call the function to get the data from the data file and store the results in lists
    airlineList, numList, departList, arriveList, costList = getData()
    # Calls the getChoice function in order to get menu choice from user
    choice = getChoice()
    while choice != 7:
        if choice == 1:
            index = findFlight(airlineList, numList)
            printResults(index, airlineList, numList, departList, arriveList, costList)
            choice = getChoice()
        elif choice == 2:
            indexList = shorterFlights(departList, arriveList)
            printResultsList(indexList, airlineList, numList, departList, arriveList, costList)
            choice = getChoice()
        elif choice == 3:
            index = cheapestFlight(airlineList, costList)
            printResults(index, airlineList, numList, departList, arriveList, costList)
            choice = getChoice()
        elif choice == 4:
            indexList = departFlght(departList)
            printResultsList(indexList, airlineList, numList, departList, arriveList, costList)
            choice = getChoice()
        elif choice == 5:
            average = averageCost(costList)
            print("The average price is $ ", average)
            choice = getChoice()
        elif choice == 6:
            indexList = timeSorted(departList)
            sortedFile(indexList, airlineList, numList, departList, arriveList, costList)
            choice = getChoice()

        else:
            choice = getChoice()
    # When choice is 7, ends loop            
    print("Thank you for flying with us")
