import time
import base64
import requests
import csv

from app_secrets import secrets

NBA_PLAYERS_LIST_ID = "17852612"

HEADER = {"Authorization": "Bearer " + secrets.BEARER_TOKEN}

#data for nodes
nbaPlayersFileName = "nbaplayers.csv"
nbaPlayersHeaders = ["id", "label"]

#Data for edges
nbaNetworkFileName = "overallNBANetwork.csv"
nbaNetworkHeaders = ["source", "target"]


def fetchNBAPlayersList():

    """
    uses the API to retrieve the ID and screenname(handle) of all NBA players in the official NBA players list
    Players list retrieved from https://twitter.com/i/lists/17852612
    See https://developer.twitter.com/en/docs/basics/cursoring for more on the logic of cursoring
    :return: an array of arrays. Each row is string array of the format [userId, screenname]
    """
    cursor = -1
    count = 5000 #max according to Twitter API documentation
    listLabelAndID = "list_id=" + NBA_PLAYERS_LIST_ID
    countLabelAndID = "&count=" + str(count)
    url = "https://api.twitter.com/1.1/lists/members.json?"
    result = []
    while cursor != 0:
        apiPath = url + listLabelAndID + countLabelAndID + "&cursor=" + str(cursor)
        response = requests.get(url=apiPath, headers=HEADER)
        responseJson = response.json()
        cursor = int(responseJson["next_cursor"])
        userList = responseJson["users"]
        for user in userList:
            userId, screenName = user["id_str"], user["screen_name"]
            print(f"found user with id {userId} and screen name {screenName}")
            if user["protected"] == False:
                result.append([userId, screenName])

    print(f"list size: {len(result)}")
    result.sort(key = lambda item: item[0])
    return result

def writeListOfStringArraysToCSV(header, data, csvFileName):
    """
    Writes the contents into a csv
    :param header: string array representing the header of the file.
            For example, a csv representing an edge list might have a header ["source", "target"]
    :param data: 2d array representing the data.
            For example, if its an edge list, we might have [["sourcenode1", "targetnode1"], ["sourcenode2, "targetnode1"]]
    :param csvFileName: name/path of csv file to put the data inside
    """

    with open(csvFileName, "w", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(header)
        csvWriter.writerows(data)


def fetchNBAPlayersUserIDsFromFile():
    """
    gets a string list of the userIds of the nba players in our network from the nbaplayer.csv file
    :return:
    """
    userIds = []
    with open(nbaPlayersFileName, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader) #move the reader cursor to next line
        # extracting each data row one by one
        for row in csvreader:
            userIds.append(row[0])
    return userIds

def checkRemainingAPICallsAvailable():
    """
    Checks how many API calls I have remaining in a given 15-minute window.
    Twitter's Standard free API allows a fixed number per 15 minute window
    :return: the number of remaining API calls I have which I can use to find a user's "friends" on twitter
    """
    apiPath = "https://api.twitter.com/1.1/application/rate_limit_status.json?resources=lists,friends"
    response = requests.get(url=apiPath, headers=HEADER)
    responseJSON = response.json()
    limit, remaining = int(responseJSON["resources"]["friends"]["/friends/ids"]["limit"]), int(responseJSON["resources"]["friends"]["/friends/ids"]["remaining"])
    print(f"limit: {limit}, remaining: {remaining}")
    return remaining


def fetchNBAPlayersSourceTargetRelationships(userIds):
    """
        uses the API to retrieve the network of nba players based on who they follow
        Players list retrieved from https://twitter.com/i/lists/17852612
        See https://developer.twitter.com/en/docs/basics/cursoring for more on the logic of cursoring
        """
    result = []
    total = len(userIds)

    # conversion helps for faster lookup. We only care about a user's "friend" if that friend's id is in this set
    userIdSet = set(userIds)

    # after every 50 users, I will write data into a csv file "nbaNetwork[batchNumber].csv"
    # doing this so that the result 2d array doesnt get *too large*, as it is cleared out after the data is written
    batchSize = 50
    batchNumber = 0

    for i in range(len(userIds)):
        userId = userIds[i]
        print(f"---------fetching data for userid {userId}------------")

        cursor = -1
        count = 5000  # max according to Twitter API documentation
        countLabelAndID = "&count=" + str(count)
        userIdAndLabel = "user_id=" + userId
        stringifyIdsAndLabels = "stringify_ids=" + "true"
        url = "https://api.twitter.com/1.1/friends/ids.json?"

        while cursor != 0:
            apiPath = url + userIdAndLabel + countLabelAndID + "&cursor=" + str(cursor) + stringifyIdsAndLabels
            if checkRemainingAPICallsAvailable() == 0:
                print("---hit API limit: will wait 15 minutes----")
                time.sleep(60 * 15)
            response = requests.get(url=apiPath, headers=HEADER)
            responseJson = response.json()
            cursor = int(responseJson["next_cursor"])
            ids = responseJson["ids"]
            for id in ids:
                if str(id) in userIdSet:
                    source, target = userId, str(id)
                    result.append([source, target])
        currentCount = i + 1
        print(f"---------finished {currentCount} out of {total} users. Just concluded data for userid {userId}------------")
        print(f"current number of edges: {len(result)}")

        # for every [batchSize] number of players we process, we write to a file and clear out the results array
        if currentCount % batchSize == 0:
            print(f"-----finished with set of 50 players...will write out current batch number {batchNumber} to csv and empty result 2d array--- ")
            newFile = "nbaNetwork" + str(batchNumber) + ".csv"
            writeListOfStringArraysToCSV(header=nbaNetworkHeaders, data=result, csvFileName=newFile)
            result = []
            print(f"-----result (edge list) has been reset to empty list now---")
            batchNumber += 1

    # write out the rest of the data in result when the for-loop is over
    print(f"-----------writing out the remaining data---------")
    newFile = "nbaNetwork" + str(batchNumber) + ".csv"
    writeListOfStringArraysToCSV(header=nbaNetworkHeaders, data=result, csvFileName=newFile)



####-------------- comment out the functions below and run the code-----------

nbaPlayersData = fetchNBAPlayersList()
writeListOfStringArraysToCSV(header=nbaPlayersHeaders, data=nbaPlayersData, csvFileName=nbaPlayersFileName)

nbaPlayersUserIds = fetchNBAPlayersUserIDsFromFile()


#### after the below script is complete,
#### Make sure to consolidate the files in "nbaNetwork0.csv", "nbaNetwork1.csv" etc into one big edge list csv.
#### I manually consolidated it into one giant edge list file called "overallNBANetwork.csv". You can do it manually or make your own script if you want
fetchNBAPlayersSourceTargetRelationships(nbaPlayersUserIds)




