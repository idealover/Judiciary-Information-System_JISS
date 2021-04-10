class Adjournment: 

    def __init__(self,date,reason):
        self._date = date
        self._reason = reason

    def reason(self):
        return self._reason
    
    def date(self):
        return self._date

