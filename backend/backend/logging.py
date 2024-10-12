import logging

class IgnoreSpecificRequests(logging.Filter):
    def filter(self, record):
        # 忽略這個日誌
        # if '/discord/get_all_sub/' in record.getMessage(): return False  
        if '/discord/get_sub/' in record.getMessage(): return False  
        # if '/discord/edit/' in record.getMessage(): return False 
        # if '/oauth/check_twitch_token/' in record.getMessage(): return False  
        
        return True  # 允許其他日誌