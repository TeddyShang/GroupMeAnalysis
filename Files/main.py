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
from datetime import datetime


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
    gTotalMessages = sum(d[0] for d in totals.values() if d) 
    gTotalLikes = sum(d[1] for d in totals.values() if d) 
    return totals, [gTotalMessages, gTotalLikes]

def getShare(stats, mInfo):
    likesGiven = []
    likesRecieved = []
    messagesSent = []
    selfLikes = []
    mstotal = 0
    lrtotal = 0
    lgtotal = 0
    sltotal = 0
    for k,v in stats.items():
        mstotal += v[0]
        lrtotal += v[1]
        lgtotal += v[2]
        sltotal += v[3]

    for k,v in stats.items():
        ms = dict()
        ms["name"] = mInfo.get(k)
        ms["value"] = v[0]
        if v[0] > 0 and v[0] > mstotal *.01 and mInfo.get(k) is not None:
            messagesSent.append(ms)

        lr = dict()
        lr["name"] = mInfo.get(k)
        lr["value"] = v[1]
        if v[1] > 0 and v[1] > lrtotal *.01 and mInfo.get(k) is not None:
            likesRecieved.append(lr)

        lg = dict()
        lg["name"] = mInfo.get(k)
        lg["value"] = v[2]
        if v[2] > 0 and v[2] > lgtotal *.01 and mInfo.get(k) is not None:
            likesGiven.append(lg)

        sl = dict()
        sl["name"] = mInfo.get(k)
        sl["value"] = v[3]
        if v[3] > 0 and v[3] > sltotal *.01 and mInfo.get(k) is not None:
            selfLikes.append(sl)
    return messagesSent,likesRecieved,likesGiven,selfLikes


def getTimeline(chatlog):
    print (len(chatlog))
    allTimeList = []
    allTime = dict()
    timeOfDayList = []
    timeOfDay = dict()
    for message in chatlog:
        timestamp = int(message.timestamp)
        strTime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        date = strTime.split(' ')[0]
        time = strTime.split(' ')[1][:-3]
        if date not in allTime:
            allTime[date] = [1, 0]
        else:
             allTime[date][0] = allTime[date][0] + 1
             allTime[date][1] = allTime[date][1] + len(message.favorited)
        if time not in timeOfDay:
            timeOfDay[time] = [1, 0]
        else:
             timeOfDay[time][0] = timeOfDay[time][0] + 1
             timeOfDay[time][1] = timeOfDay[time][1] + len(message.favorited)
       
    for k,v in allTime.items():
        allTimeList.append({'date':k,'messages':v[0], 'likes': v[1]})

    for k,v in timeOfDay.items():
        timeOfDayList.append({'time':k,'messages':v[0], 'likes': v[1]})

    return allTimeList, timeOfDayList





if __name__ == "__main__":
    main()

