

class Snake:
    def __init__(self, head, body):
        self.head = head
        self.body = body
        self.direction = "right"
        self.length = 1

    def move(self):
        self.head.x += 1
        self.body.append(self.head)
        if len(self.body) > self.length:
            self.body.pop(0)

    def get_head(self):
        return self.head
    
    def get_body(self):
        return self.body
    
    def get_length(self):
        return self.length
    
    def grow(self):
        self.length += 1
    