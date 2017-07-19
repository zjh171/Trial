class Trial():
    trialId = ""
    mediName = ""
    mediSort = ""
    trialType = ""
    registerSort = ""
    companyName = ""
    startDate = ""

    def __init__(self):
        return
    def __str__(self):
        return self.trialId + self.mediName + self.mediSort + self.trialType + self.registerSort + self.companyName + str(self.startDate)