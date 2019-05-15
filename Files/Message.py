class Message:
    def __init__(self, created_at, favorited, messageId, senderId, text, attachments):
        self.timestamp = created_at
        self.favorited = favorited
        self.messageId = messageId
        self.senderId = senderId
        self.text = text
        self.attachments = attachments