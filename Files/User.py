import Values
from Group import Group
from Member import Member
import requests, json

class User:
    def __init__(self, devToken):
        self.devToken = devToken
        self.groups = []

    def getGroups(self):
        page = 1;
        while True:
            request = requests.get(Values.apiGroupsBaseUrl, params={'token':self.devToken, 'page':page})
            if request.status_code != 200:
                return
            text = json.loads(request.text)
            jsonGroups = text['response']
            if len(jsonGroups) == 0:
                break;
            page = page + 1
            for jsonGroup in jsonGroups:
                name = jsonGroup['name']
                description= jsonGroup['description']
                imageUrl= jsonGroup['image_url']
                created_at= jsonGroup['created_at']
                updated_at= jsonGroup['updated_at']
                groupId= jsonGroup['group_id']
                jsonMembersList= jsonGroup['members']
                membersList = []
                for members in jsonMembersList:
                    memberId = members['user_id']
                    memberName = members['nickname']
                    memberImageUrl = members['image_url']
                    memberRoles = members['roles']
                    member = Member(memberId, memberName, memberImageUrl, memberRoles)
                    membersList.append(member)
                group = Group(name, description, imageUrl, created_at, updated_at, groupId, membersList)
                self.groups.append(group)
