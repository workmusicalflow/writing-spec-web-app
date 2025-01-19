class ContextManager:
    def __init__(self):
        self.user_input = ""
    
    def set_user_input(self, input_text):
        self.user_input = input_text
    
    def get_user_input(self):
        return self.user_input
