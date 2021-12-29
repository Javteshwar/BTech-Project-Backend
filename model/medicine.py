class Medicine:
    medid=int
    name=str
    diseaseid=int

    def __init__(self,medid=-1,name='',diseaseid=-1):
        self.medid=medid
        self.name=name
        self.diseaseid=diseaseid