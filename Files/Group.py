class Group:
    def __init__(self, name, description, imageUrl, created_at, updated_at, groupId, membersList):
        self.name = name
        self.description = description
        self.imageUrl = imageUrl
        self.created = created_at
        self.updated = updated_at
        self.id = groupId
        self.members = membersList