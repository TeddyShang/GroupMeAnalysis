##GroupMe textual analysis and visualization of various features
##Requires API Key, GroupId
##Planned features
##CSV of metrics such as: Total Likes, Total Messages, Likes Given, Self Likes
##Saved Chat Conversation in .txt file
##Eventually data viz of chat timeline "spikes"
##Node graph of who likes who...
##Mentions?

#import requests, time, json, sys, io
from User import User
from Group import Group
from Member import Member
from Message import Message
import Secrets



def main(devToken):
    #user = User(devToken)
    #user.getGroups()
    #return user.groups
    #chatlog = user.groups[1].getChatLog()
    return

def getGroups(devToken):
    user = User(devToken)
    user.getGroups()
    if len(user.groups) == 0:
        return None
    return user.groups


if __name__ == "__main__":
    main()

#legacy code
#chatlog = open('chatlog.txt', 'wb')

#apiGroupsBaseUrl = 'https://api.groupme.com/v3/groups/'
###format. Key: user_id, Value = [name, MessagesSent, Likes Received, Likes Given, Self Likes]
#csvDict = dict();

###Initial call to get last before_id
#request = requests.get(apiGroupsBaseUrl + groupId + '/messages?token=' + devToken, params={'limit':'100'})
#text = json.loads(request.text);
#messages = text['response']['messages']
#lastEntry = ''

###for debug purposes
#counter = 0

#def likesGiven(message):
#    global csvDict
#    messageLikes = message['favorited_by']
#    name = message['name']
#    for user in messageLikes:
#        if user not in csvDict:
#            csvDict[user] = ['Temp', 0, 0, 0, 0]
#        oldInfo = csvDict.get(user)
#        oldInfo[3] = oldInfo[3] + 1
#        csvDict[user] = oldInfo

#def likesRecieved(message):
#    global csvDict
#    messageLikes = message['favorited_by']
#    userId = message['user_id']
#    oldInfo = csvDict.get(userId)
#    oldInfo[2] = oldInfo[2] + len(messageLikes)
#    csvDict[userId] = oldInfo


#def likesSelf(message):
#    global csvDict
#    messageLikes = message['favorited_by']
#    userId = message['user_id']
#    if userId in messageLikes:
#        oldInfo = csvDict.get(userId)
#        oldInfo[4] = oldInfo[4] + 1
#        csvDict[userId] = oldInfo

#def writeToLog(message):
#    global chatlog
#    wName = message['name']
#    wText = message['text']
#    messageLikes = message['favorited_by']
#    wMessage = wName + ' [' + str(len(messageLikes))+ ']'+':' + wText + '\n'
#    chatlog.write(wMessage.encode('utf-8'))
#    return

#def totalMessagesSents(message):
#    global csvDict
#    userId = message['user_id']
#    oldInfo = csvDict.get(userId)
#    oldInfo[1] = oldInfo[1] + 1
#    csvDict[userId] = oldInfo


#for message in messages:
#    if(message['text'] != None):
#        writeToLog(message)
#        userId = message['user_id']
#        name = message['name']
#        if userId not in csvDict:
#            csvDict[userId] = [name, 0, 0, 0, 0]
#        nameChange = csvDict.get(userId)
#        nameChange[0] = name
#        csvDict[userId] = nameChange
#        likesGiven(message)
#        likesRecieved(message)
#        likesSelf(message)
#        totalMessagesSents(message)
#    lastEntry = message['id']

#while(True):
#    request = requests.get(apiGroupsBaseUrl + groupId + '/messages?token=' + devToken, params={'limit':'100', 'before_id': lastEntry})
#    try:
#        text = json.loads(request.text);
#        messages = text['response']['messages']
#    except ValueError:
#        print("End of messages")
#        break
#    for message in messages:
#        if(message['text'] != None):
#            writeToLog(message)
#            userId = message['user_id']
#            name = message['name']
#            if userId not in csvDict:
#                csvDict[userId] = [name, 0, 0, 0, 0]
#            nameChange = csvDict.get(userId)
#            nameChange[0] = name
#            likesGiven(message)
#            likesRecieved(message)
#            likesSelf(message)
#            totalMessagesSents(message)
#        lastEntry = message['id']
#    time.sleep(.5)
#    counter= counter + 1
#    print(counter)

#chatlog.close()
#for k,v in csvDict.items():
#    print (k,"=>", v)

