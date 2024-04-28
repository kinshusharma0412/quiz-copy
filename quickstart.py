#!/usr/bin/python

import json
import io
import re as reaaa
import pickle
import os.path
try:
	from googleapiclient.discovery import build
except:
	from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

def my(a,b):
	import xlsxwriter
	db={}
	ndb=[]
	no_que=0
	for x in a['items']:
		if x['title']=='Your Name':
			ndb.append(x['questionItem']['question']['questionId'])
		elif 'pageBreakItem' in x:
		    pass

		elif 'grading' in x['questionItem']['question']:
			db[x['questionItem']['question']['questionId']]=[x['questionItem']['question']['grading']['correctAnswers']['answers'][y]['value'] for y in range(len(x['questionItem']['question']['grading']['correctAnswers']['answers']))]
			no_que+=1
	#print(ndb)
	result=[]
	for x in b['responses']:
		right=0
		wrong=0
		for y in x['answers'].keys():
			if y in db.keys():
				if x['answers'][y]['textAnswers']['answers'][0]['value'] in db[y]:
					right+=1
				else:
					wrong+=1
			elif y in ndb:
				name=x['answers'][y]['textAnswers']['answers'][0]['value']
		result.append({"rank":None,"name":name,"total":4*right-wrong,"right":right,"wrong":wrong,"skip":no_que-right-wrong})
	temp=[]
	#print(result)
	def myFunc(e):
		return e['total']
	result.sort(reverse=True,key=myFunc)
	Ttt=0
	nn=1
	for x in range(len(result)):
	    if result[x]["total"]==Ttt:
	        result[x]["rank"]=nn
	    else:
	        Ttt=result[x]["total"]
	        result[x]["rank"]=x+1
	        nn=x+1
	data=[]
	for x in range(len(result)):
	    #data[x]=[]
	    data.append([(result[x]['rank']),result[x]['name'],(result[x]['total']),(result[x]['right']),(result[x]['wrong']),result[x]["skip"]])

	#print(data)
	workbook = xlsxwriter.Workbook(str(a['info']['title'])+'.xlsx')
	worksheet = workbook.add_worksheet()
	fa=workbook.add_format()
	fa.set_align('center')

	worksheet.set_column('A:A', 5)
	worksheet.set_column('B:B', 45,fa)
	worksheet.set_column('C:C', 9)
	worksheet.set_column('D:D', 9)
	worksheet.set_column('E:E', 9)
	worksheet.set_column('F:F', 9)
	worksheet.add_table('A1:F'+str(len(result)+1), {'data': data,'columns': [{'header': 'Rank'},{'header': 'Name'},{'header': 'Marks'},{'header': 'Right'},{'header': 'Wrong'},{'header': 'Skip'}]})
	workbook.close()

	return str(a['info']['title'])+'.xlsx'

def my1(a,b):
	import xlsxwriter
	db={}
	ndb=[]
	pdb=[]
	mdb=[]
	no_que=0
	print (a['items'])
	for x in a['items']:
		
		print (x)
		if x['title']=='Gmail':
			mdb.append(x['questionItem']['question']['questionId'])
		if x['title']=='Your Name':
			ndb.append(x['questionItem']['question']['questionId'])
		if x['title']=='Password':
			pdb.append(x['questionItem']['question']['questionId'])
		elif 'pageBreakItem' in x:
		    pass

		elif 'grading' in x['questionItem']['question']:
			yyyy=[]
			for y in range(len(x['questionItem']['question']['grading']['correctAnswers']['answers'])):
			    yyyy.append(x['questionItem']['question']['grading']['correctAnswers']['answers'][y]['value'])
			db[x['questionItem']['question']['questionId']]=yyyy
			no_que+=1
	#print(ndb)
	result=[]
	for x in b['responses']:
		right=0
		wrong=0
		mail=None
		password="None"
		for y in x['answers'].keys():
			#print(y)
			if y in db.keys():
				if x['answers'][y]['textAnswers']['answers'][0]['value'] in db[y]:
					right+=1
				else:
					wrong+=1
			elif y in ndb:
				name=x['answers'][y]['textAnswers']['answers'][0]['value']
			elif y in pdb:
				try:
				    password=x['answers'][y]['textAnswers']['answers'][0]['value']
				except:
				    password="None"
			elif y in mdb:
				try:
				    mail=x['answers'][y]['textAnswers']['answers'][0]['value']
				except:
				    mail=None
		result.append({"rank":None,"mail":mail,"name":name,"password":password,"total":4*right-wrong,"right":right,"wrong":wrong,"skip":no_que-right-wrong})
	temp=[]
	def myFunc(e):
		return e['total']
	result.sort(reverse=True,key=myFunc)
	for x in range(len(result)):
	    result[x]["rank"]=x+1
	data=[]
	for x in range(len(result)):
	    #data[x]=[]
	    data.append({"rank":(result[x]['rank']),"mail":result[x]['mail'],"name":result[x]['name'],"password":result[x]['password'],"total":(result[x]['total']),"right":(result[x]['right']),"wrong":(result[x]['wrong']),"skip":result[x]["skip"]})

	[print(x) for x in data]
	return (data)
	
def my3(a,b):
	import xlsxwriter
	db={}
	ndb=[]
	pdb=[]
	no_que=0
	print (a['items'])
	for x in a['items']:
		
		if x['title']=='Your Name':
			ndb.append(x['questionItem']['question']['questionId'])
		if x['title']=='Password':
			pdb.append(x['questionItem']['question']['questionId'])
		
	result=[]
	for x in b['responses']:
		
		for y in x['answers'].keys():
			
			if y in ndb:
				name=x['answers'][y]['textAnswers']['answers'][0]['value']
			elif y in pdb:
				try:
				    password=x['answers'][y]['textAnswers']['answers'][0]['value']
				except:
				    password="None"
		result.append({"name":name,"password":password})
	
	return result

class Drive_OCR:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.SCOPES = ['https://www.googleapis.com/auth/script.projects','https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/drive']
        self.credentials = "./credentia.json"
        self.pickle = "token.pickle"
        #print(self.filename)
    
    def copy_file(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        
            # pylint: disable=maybe-no-member
        response = service.files().copy(
        fileId=id, body={'title': "Question Bank"}).execute()
        dic=[]
        
        return response.get('id')
    def google_drive_get(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        
            # pylint: disable=maybe-no-member
        response = service.files().list(q="mimeType='application/vnd.google-apps.form'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id)',
                                            pageToken=page_token).execute()
        dic=[]
        for x in response["files"]:
        	
        	if x['id'].startswith(id):
        	    dic.append(x['id'])
        	
        
        	
        
        return (dic)
    
        #body =body={ "requests": self.filename}
            
        
    
    def google_spreadsheet_get(self,id,range_name) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(spreadsheetId=id, range=range_name).execute()
        return (result.get('values', []))
        
    def google_spreadsheet_update(self,id, range_name, value_input_option,
                  _values) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('sheets', 'v4', credentials=creds)
        value_input_option
        values = _values
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(spreadsheetId=id, range=range_name,valueInputOption=value_input_option, body=body).execute()
        return (result.get('values', []))
    
    def google_sheet_create(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('sheets', 'v4', credentials=creds)
    
        body=  self.filename
            
        doc = service.spreadsheets().create(body=body).execute()
        return doc
        
    def google_form_get(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        #body =body={ "requests": self.filename}
            
        doc1 = service.forms().get(formId=id).execute()
        link=doc1.get('responderUri')
        doc2 = service.forms().responses().list(formId=id).execute()
        #print(doc1)
        
        
        return my(doc1,doc2), link
    def google_form_id_responce(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        #body =body={ "requests": self.filename}
            
        doc1 = service.forms().get(formId=id).execute()
        link=doc1.get('responderUri')
        #doc2 = service.forms().responses().list(formId=id).execute()
        #print(doc1)
        
        
        return id, link

        
    def google_form_get1(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        #body =body={ "requests": self.filename}
            
        doc1 = service.forms().get(formId=id).execute()
        link=doc1.get('responderUri')
        doc2 = service.forms().responses().list(formId=id).execute()
        
        
        return my1(doc1,doc2), link
    def google_form_get2(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        nfl=[]
        for x in id:
            try:
                doc1 = service.forms().get(formId=x).execute()
                doc2 = service.forms().responses().list(formId=x).execute()
                for y in my3(doc1,doc2):
                    nfl.append(y)
            except:
                pass
        
        
        return nfl

    def google_form_responce_url(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        #body =body={ "requests": self.filename}
            
        doc1 = service.forms().get(formId=id).execute()
        link=doc1.get('responderUri')
        #doc2 = service.forms().responses().list(formId=id).execute()
        #print(doc1)
        
        
        return link
        
    def google_form_create(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        body={"info":self.filename}
            
        doc = service.forms().create(body=body).execute()
        print(doc)
        drive_service = build('drive', 'v3', credentials=creds)
        file_id = doc.get('formId')
        folder_id = "10qRK4F2JWB6rzxo9ZsSOL-tiG6UsLNoD"
        file = drive_service.files().get(fileId=file_id, fields='parents').execute()
        print(file)
        previous_parents = ",".join(file.get('parents'))
        print(previous_parents)
        file = drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
        print(file)
        return doc
        
    def google_form_update(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('forms', 'v1', credentials=creds)
    
        body={ "requests": self.filename}
            
        doc = service.forms().batchUpdate(body=body,formId=id).execute()
        return doc
        
    def create(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        
        service = build('docs', 'v1', credentials=creds)
    
        body = {"title": 'Result.pdf'}
            
        doc = service.documents().create(body=body).execute()
        
        return doc.get('documentId')
        
    def move(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)
        file_id = id
        folder_id = "1uM8En7yQEUsaJLVnePlifqE_hqn9_PKj"
        drive_service = build('drive', 'v3', credentials=creds)
        file = drive_service.files().get(fileId=file_id, fields='parents').execute()
        print(file)
        previous_parents = ",".join(file.get('parents'))
        print(previous_parents)
        file = drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
    def update(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)
        service = build('docs', 'v1', credentials=creds)
        body=self.filename
        doc1 = service.documents().batchUpdate(body=body,documentId=id).execute()
        return doc1
        
    def download(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)
        service = build('drive', 'v3', credentials=creds)
        request = service.files().export_media(fileId=id,mimeType='application/pdf')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
                
        fh.seek(0)
        import shutil
        shutil.copyfileobj(fh,open(reaaa.sub("\.(txt|jpeg|jpg|png)","","Result")+".pdf", 'wb'))
        return reaaa.sub("\.(txt|jpeg|jpg|png)","","Result")+".pdf"
    def delete(self,id) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)
        service = build('drive', 'v3', credentials=creds)
        service.files().delete(fileId=id).execute()

        


    def main(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        print('File ID: %s' % file.get('id'))

        # It will export drive image into Doc
        request = service.files().export_media(fileId=file.get('id'),mimeType="text/plain")

        # For Downloading Doc Image data by request
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        # It will delete file from drive base on ID
        service.files().delete(fileId=file.get('id')).execute()

        # It will print data into terminal
        output = fh.getvalue().decode()
        return output

    def main1(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        file_id = file.get('id')
        folder_id = "1uM8En7yQEUsaJLVnePlifqE_hqn9_PKj"
        drive_service = build('drive', 'v3', credentials=creds)
        file1 = drive_service.files().get(fileId=file_id, fields='parents').execute()
        
        previous_parents = ",".join(file1.get('parents'))
        #print(previous_parents)
        file2 = drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()
        request = service.files().export_media(fileId=file.get('id'),mimeType='application/pdf')
        print(request)
        
#        

#        # For Downloading Doc Image data by request
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        #open("Result.pdf", "wb").write(fh)

        # It will delete file from drive base on ID
        fh.seek(0)
        import shutil
        shutil.copyfileobj(fh,open(self.filename[:-5]+".pdf", 'wb'))
        service.files().delete(fileId=file.get('id')).execute()
        return self.filename[:-5]+".pdf"

    def main2(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        
        request = service.files().export_media(fileId=file.get('id'),mimeType='application/pdf')
        print(request)
        
#        

#        # For Downloading Doc Image data by request
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        #open("Result.pdf", "wb").write(fh)

        # It will delete file from drive base on ID
        service.files().delete(fileId=file.get('id')).execute()
        fh.seek(0)
        import shutil
        shutil.copyfileobj(fh,open(reaaa.sub("\.(txt|jpeg|jpg|png)","",self.filename)+".pdf", 'wb'))

        # It will print data into terminal
        #output = fh.getvalue().decode()
        return reaaa.sub("\.(txt|jpeg|jpg|png)","",self.filename)+".pdf"

    def main3(self) -> str:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        import xlsxwriter
        workbook=xlsxwriter.Workbook(self.filename)
        worksheet = workbook.add_worksheet()
        workbook.close()

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        print(file)
        print(file['id'])
        return file['id']
        
        #
        
