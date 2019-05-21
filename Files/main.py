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

def getChatlog(groupId, devToken):
    group = Group(groupId = groupId)
    group.getGroupInformation(devToken)
    return group.getChatLog(devToken)

def getMemberInformation(groupId, devToken):
    group = Group(groupId = groupId)
    group.getGroupInformation(devToken)
    members = group.allMembers
    return members
 
def likesGiven(totals, message):
    messageLikes = message.favorited
    for user in messageLikes:
        if user not in totals:
            totals[user] = [0, 0, 0, 0]
        oldInfo = totals.get(user)
        oldInfo[2] = oldInfo[2] + 1
        totals[user] = oldInfo

def likesRecieved(totals, message):
    messageLikes = message.favorited
    userId = message.senderId
    oldInfo = totals.get(userId)
    oldInfo[1] = oldInfo[1] + len(messageLikes)
    totals[userId] = oldInfo


def likesSelf(totals, message):
    messageLikes =message.favorited
    userId = message.senderId
    if userId in messageLikes:
        oldInfo = totals.get(userId)
        oldInfo[3] = oldInfo[3] + 1
        totals[userId] = oldInfo

def totalMessagesSents(totals, message):
    userId = message.senderId
    oldInfo = totals.get(userId)
    oldInfo[0] = oldInfo[0] + 1
    totals[userId] = oldInfo

##what kind of information do we want?
#most messages, most likes accepted, average likes, most likes given, self likes
###format. Key: user_id, Value = [MessagesSent, Likes Received, Likes Given, Self Likes]
def getStats(chatlog):
    totals = dict()
    for message in chatlog:
        userid = message.senderId
        if userid not in totals:
            totals[userid] = [0, 0, 0, 0]
        likesGiven(totals, message)
        likesRecieved(totals, message)
        likesSelf(totals,message)
        totalMessagesSents(totals,message)
    return totals

if __name__ == "__main__":
    main()

