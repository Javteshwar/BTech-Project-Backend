class LabReport:
    labid=int
    patientid=int
    labname=str
    resultstatus=bool

    def __init__(self,labid=-1,patientid=-1,labname='',resultstatus=True):
        self.labid=labid
        self.patientid=patientid
        self.labname=labname
        self.resultstatus=resultstatus