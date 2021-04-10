from .Adjournment import Adjournment
from .Hearing import Hearing

class Case:
    # _defendantName = ""
    # _defendantAddr = ""
    # _crimeType = ""
    # _crimeDate = ""
    # _crimeLocation = ""
    # _officerName = ""
    # _arrestDate = ""
    # _dateOfHearing = ""
    # _judgeName = ""
    # _prosecutorName = ""
    # _caseStatus = ""
    # caseJudgement = ""
    # _adjs = []
    # _hearings = []
    # CIN = 0
    # startDate = ""
    # endDate = ""
    # nextCIN = 1 #next available CIN

    def __init__(self,details):
        self.CIN_ = details[0]
        self.defendantName_ = details[1]
        self.defendantAddress_ = details[2]
        self.crimeType_ = details[3]
        self.crimeDate_ = details[4]
        self.crimeLocation_ = details[5]
        self.officerName_ = details[6]
        self.arrestDate_ = details[7]
        self.judgeName_ = details[8]
        self.lawyerName_ = details[9]
        self.prosecutorName_ = details[10]
        self.startingDate_ = details[11]
        self.caseStatus_ = details[12]
        self.caseSummary_ = details[13]
        self.endDate_ = details[14]
        self.dateOfHearing_ = details[15]
        self.adjournments_ = details[16]
        self.hearings_ = details[17]
        self.judgement_ = details[18]
    
    def getCaseDetails(self):
        ans = [self.CIN_,self.defendantName_,self.defendantAddress_ ,self.crimeType_,
        self.crimeDate_,
        self.crimeLocation_,
        self.officerName_ ,
        self.arrestDate_,
        self.judgeName_ ,
        self.lawyerName_,
        self.prosecutorName_ ,
        self.startingDate_,
        self.caseStatus_ ,
        self.caseSummary_,
        self.endDate_,
        self.dateOfHearing_,
        self.adjournments_,
        self.hearings_,
        self.judgement_]

        return ans

    def getCaseStatus(self):
        return self.caseStatus_

    def adjourn(self,date,reason):
        # temp = Adjournment(date,reason)
        self.adjournments_.append([date,reason])

    def newhearing(self,hearingg):
        self.hearings_.append(hearingg)


    def closeCase(self,date,summary):
        self.endDate_ = date
        self.caseStatus_ = "Closed"
        self.caseSummary_ = summary
        # self.case