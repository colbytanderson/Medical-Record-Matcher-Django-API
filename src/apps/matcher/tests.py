from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model as user_model
User = user_model()
from rest_framework.test import force_authenticate
import io
from rest_framework.parsers import JSONParser
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import os
from apps.matcher.main.models import Record, Column

class RecordViewSetTest(APITestCase):

    def setUp(self):
        # create user
        self.user = User(username='a')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.record = Record(owner=self.user, title='Test', confidenceScore=0.68,
                            fullNameConfidenceScore=0.1)
        self.record.editors.add(self.user)
        self.record.save()


    # ("firstname", "firstname"),
    # ("middlename", "middlename"),
    # ('accountnumber', 'accountnumber'),
    # ('lastname', 'lastname'),
    # ('dob', 'dob'), # date of birth
    # ('sex', 'sex'),
    # ('street', 'street'),
    # ('city', 'city'),
    # ('state', 'state'),
    # ('zip', 'zip'),



        # fake col 0
        self.column0 = Column(record=self.record, title='Col0', dataType='zip',
                            confidenceScore=0.44, index=0)
        self.column0.save()
        # fake col 1
        self.column1 = Column(record=self.record, title='Col1', dataType='zip',
                            confidenceScore=0.44, index=1)
        self.column1.save()
        # 2 PAN_WEIGHT = 0.01
        self.column2 = Column(record=self.record, title='Col2', dataType='accountnumber',
                            confidenceScore=0.01, index=2)
        self.column2.save()
        # 3 first CN_WEIGHT = 0.1
        self.column3 = Column(record=self.record, title='Col3', dataType='firstname',
                            confidenceScore=0.05, index=3)
        self.column3.save()
        # 4 CMI_WEIGHT = 0.01
        self.column4 = Column(record=self.record, title='Col4', dataType='middlename',
                            confidenceScore=0.01, index=4)
        self.column4.save()
        # 5 last CN_WEIGHT = 0.1
        self.column5 = Column(record=self.record, title='Col5', dataType='lastname',
                            confidenceScore=0.05, index=5)
        self.column5.save()
        # DOB_WEIGHT = 0.06
        self.column6 = Column(record=self.record, title='Col6', dataType='dob',
                            confidenceScore=0.06, index=6)
        self.column6.save()
        # S_WEIGHT = 0.04
        self.column7 = Column(record=self.record, title='Col6', dataType='sex',
                            confidenceScore=0.04, index=7)
        self.column7.save()
        # CS1_WEIGHT = 0.2
        self.column8 = Column(record=self.record, title='Col8', dataType='street',
                            confidenceScore=0.2, index=8)
        self.column8.save()
        # CS2_WEIGHT = 0.01
        self.column9 = Column(record=self.record, title='Col9', dataType='street',
                            confidenceScore=0.01, index=9)
        self.column9.save()
        # CC_WEIGHT = 0.07
        self.column10= Column(record=self.record, title='Col10', dataType='city',
                            confidenceScore=0.07, index=10)
        self.column10.save()
        # CS_WEIGHT = 0.07
        self.column11 = Column(record=self.record, title='Col11', dataType='state',
                            confidenceScore=0.07, index=11)
        self.column11.save()
        # CZ_WEIGHT = 0.03
        self.column12 = Column(record=self.record, title='Col12', dataType='zip',
                            confidenceScore=0.03, index=12)
        self.column12.save()
        # PN_WEIGHT = 0.05
        self.column13 = Column(record=self.record, title='Col13', dataType='firstname',
                            confidenceScore=0.025, index=13)
        self.column13.save()
        # PMI_WEIGHT = 0.01
        self.column14 = Column(record=self.record, title='Col14', dataType='middlename',
                            confidenceScore=0.01, index=14)
        self.column14.save()
        # PN_WEIGHT = 0.05
        self.column15 = Column(record=self.record, title='Col15', dataType='lastname',
                            confidenceScore=0.025, index=15)
        self.column15.save()
        # PS1_WEIGHT = 0.16
        self.column16 = Column(record=self.record, title='Col16', dataType='street',
                            confidenceScore=0.16, index=16)
        self.column16.save()
        # PS2_WEIGHT = 0.01
        self.column17 = Column(record=self.record, title='Col17', dataType='street',
                            confidenceScore=0.01, index=17)
        self.column17.save()
        # PC_WEIGHT = 0.07
        self.column18 = Column(record=self.record, title='Col18', dataType='city',
                            confidenceScore=0.07, index=18)
        self.column18.save()
        # PS_WEIGHT = 0.07
        self.column19 = Column(record=self.record, title='Col19', dataType='state',
                            confidenceScore=0.07, index=19)
        self.column19.save()
        # PZ_WEIGHT = 0.03
        self.column20 = Column(record=self.record, title='Col20', dataType='zip',
                            confidenceScore=0.03, index=20)
        self.column20.save()











    def tearDown(self):
        pass

    def testCreateBasic(self):
        pass

    def testAddColumnBasic(self):
        pass

    def testMatchRowsBasicFunctionality(self):
        # os.path.join
        base_path = os.path.dirname(os.path.realpath(__file__))
        pat = base_path + "/medicalRecords.csv"
        data = open(pat, 'rb')
        file = SimpleUploadedFile("medicalRecords.csv", data.read(), content_type="text/csv")
        response = self.client.post('/matcher/Test/matchRows/', {'file': file})
        print(response.data)
