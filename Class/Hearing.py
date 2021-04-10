class Hearing:

    def __init__(self,date,summary):
        self._date = date
        self._summary = summary

    def date(self):
        return self._date

    def hearing(self):
        return self._summary

    def give(self):
    	temp = []
    	temp.append(self._date)
    	temp.append(self._summary)
    	return temp