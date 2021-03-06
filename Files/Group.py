import Values
from Message import Message
import requests, json
import Member

class Group:
    def __init__(self, name="", description="", imageUrl="", created_at=0, updated_at=0, groupId=0, currentMembersList=[], allMembersList = dict()):
        self.name = name
        self.description = description
        self.imageUrl = imageUrl
        self.created = created_at
        self.updated = updated_at
        self.id = groupId
        self.currentMembers = currentMembersList
        self.allMembers = allMembersList

    def getGroupInformation(self, devToken):
        request = requests.get(Values.apiGroupsBaseUrl + '/' + self.id,  params={'token':devToken})
        text = json.loads(request.text)
        self.name = text['response']['name']
        self.description = text['response']['description']
        self.imageUrl = text['response']['image_url']
        self.created = text['response']['created_at']
        self.updated = text['response']['messages']['last_message_created_at']
        members = text['response']['members']
        currentMembers = []
        for member in members:
            id = member['user_id']
            name = member['nickname']
            image = member['image_url']
            role = member['roles'][0]
            m = Member.Member(id, name, image, role)
            currentMembers.append(m)
        self.currentMembers = currentMembers

    def getChatLog(self,devToken):
        chatlog = []
        request = requests.get(Values.apiGroupsBaseUrl + '/' + self.id + '/messages',  params={'token':devToken, 'limit':1})
        if request.status_code != 200:
            return chatlog;
        text = json.loads(request.text);
        messages = text['response']['messages']
        ftimestamp = messages[0]['created_at']
        ffavorited = messages[0]['favorited_by']
        fmessageId = messages[0]['id']
        fsenderId = messages[0]['sender_id']
        ftext = messages[0]['text']
        fattachments = messages[0]['attachments']
        firstMessage = Message(ftimestamp, ffavorited, fmessageId, fsenderId, ftext, fattachments)
        chatlog.append(firstMessage)
        lastEntry = fmessageId
        while True:
            request = requests.get(Values.apiGroupsBaseUrl + '/' + self.id + '/messages',  params={'token':devToken, 'limit':100, 'before_id': lastEntry})
            if request.status_code == 304:
                break;
            text = json.loads(request.text);
            messages = text['response']['messages']
            for message in messages:
                timestamp = message['created_at']
                favorited = message['favorited_by']
                messageId = message['id']
                senderId = message['sender_id']
                text = message['text']
                attachments = message['attachments']
                cMessage = Message(timestamp, favorited, messageId, senderId, text, attachments)
                chatlog.append(cMessage)
                if senderId not in self.allMembers:
                    self.allMembers[senderId] = message['name']
            lastEntry = messageId
        return chatlog 