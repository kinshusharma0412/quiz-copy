#!/usr/bin/env python
# -*- coding: utf-8 -*-
print("started")
#Profile_photo_soojh=[-1001536663326,-1001375781470,-1001360402430,-1001500806585,-1001472812678,-1001145720099,-1001373589965]
skip_group=[-1001465228197,-1001829885432]
import random,string
def id_generator(size=10, chars=string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))
import time,datetime
#from deep_translator import GoogleTranslator
import re as reaaa
from pymongo import MongoClient
import dns
import os
import traceback
import streamlit as st
from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone="Asia/kolkata")
scheduler.start()
#import dns.resolver
#dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
#dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server,  use whatever dns server you like here
# as a test, dns.resolver.query('www.google.com') should return an answer, not an exception'''

clientmongo=MongoClient('mongodb+srv://'+os.environ.get('mongo',"")+'.ckcyx.mongodb.net/test?retryWrites=true&w=majority')
list_sub=[reaaa.sub("(^ {1,}| {1,}$)","",x) for x in clientmongo["channal"]["sub"].find_one({"db":{"$type":"array"}})["db"]]
from pyrogram import Client, enums
from pyrogram.methods.utilities.idle import idle
from urllib.parse import quote_plus
from pyrogram.raw import functions
from pyrogram.raw import types
from pyrogram.handlers import MessageHandler, PollHandler
from pyrogram import filters
from pyrogram.types import Message, ReplyKeyboardRemove, Poll,MenuButtonWebApp,WebAppInfo,MenuButtonCommands,MessageEntity,MenuButtonCommands
from pyrogram.types import ReplyKeyboardMarkup as RKM
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.enums import PollType,MessageEntityType
from pyrogram.raw.functions.messages import ForwardMessages
from pyrogram.raw.functions.channels import GetFullChannel, EditAdmin
from pyrogram.raw.types import ChatAdminRights
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from pyrogram.errors import FloodWait
import  json
import time
#from quickstart import Drive_OCR
import requests
import asyncio


def resub(x):
	x=reaaa.sub("◄.*(⎯꯭|⎯꯭‌){1,}","",x)
	for z in list_sub:
		x=reaaa.sub("( {1,}|\n{1,}|)"+z+"( {1,}|\n{1,}|)","",x)
	return x

app = Client("Guru",
session_string=os.environ.get('app_session_string',""),
api_id=os.environ.get('api_id',""),
api_hash=os.environ.get('api_hash',""))

app_bot=Client(id_generator(),
bot_token=os.environ.get('bot_token',""),api_id=os.environ.get('api_id',""),
api_hash=os.environ.get('api_hash',""))

polls_extractor = Client("polls_extractor",
session_string=os.environ.get('polls_extractor',""),
api_id=os.environ.get('api_id',""),
api_hash=os.environ.get('api_hash',""))

def aadmiL(data):
    async def quizbot_d(_, c: Client, m: Message):
        #print(m.from_user)
        try:
            user_id=m.from_user.id
            if user_id in cm["addmi"]["Live_Quiz"].find_one({"admin":{"$type":"array"}})["admin"]:
            	return True
            else:
            	await c.send_message(m.chat.id,"You are not admin of this command\n\nbot admin username:- "+data)
        except:
            await c.send_message(m.chat.id,"You are not admin of this command")
            return False
    return filters.create(quizbot_d,data=data)

#&  filters.chat([-1001465228197,-1002102245244,-1002102245244,-1001942625594]
@app.on_message(filters.photo & filters.incoming & ~ filters.private)
async def photo_dhankad(client:Client,message:Message):
	poll_topic=clientmongo["ajay"]["poll"].find_one({str(message.chat.id):{"$type":"string"}})
	if poll_topic is not None:
		topic=poll_topic[str(message.chat.id)]
		fname=id_generator()
		file=await app.download_media(message,file_name=fname+"sample.png")
		#await app.send_message(message.chat.id, str(file))
		
		await app.send_photo(-1002056439885,photo=file, caption=message.photo.caption,reply_to_message_id=int(topic))


@app.on_message(filters.regex("\.add") & filters.private)#& filters.incoming & filters.private)
async def job2_parteggnegr(client:Client,message:Message):
	global list_sub
	await app.send_message(message.chat.id, str("start"))
	text=reaaa.split("\n{1,}",message.text)
	for x in text[1:]:
		if x not in list_sub:
			list_sub.append(x)
	clientmongo["channal"]["sub"].find_one_and_update({"db":{"$type":"array"}},{ "$set": {"db":list_sub}})
	await app.send_message(message.chat.id, str("done"))
@app.on_message(filters.regex("The quiz")  )#& filters.incoming )
async def job2_partener(client:Client,message:Message):
	new_text=""
	if message.reply_markup:
		if message.reply_markup.inline_keyboard[0][0].text=="Share quiz":
			if message.reply_markup.inline_keyboard[0][0].switch_inline_query.startswith("quiz:"):
				await app.send_message(-1002120636417, "`"+reaaa.sub("quiz:","/start@quizbot ",message.reply_markup.inline_keyboard[0][0].switch_inline_query)+"`\n\n"+reaaa.sub(" ","_","#"+message.chat.title))
				chose=await app.get_inline_bot_results("quizbot", message.reply_markup.inline_keyboard[0][0].switch_inline_query)
				await app.send_inline_bot_result(
chat_id=-1002120636417,
query_id=chose.query_id,
result_id=chose.results[0].id)
next=0			

#@app.on_message(filters.poll & filters.incoming & ~ filters.chat([-1002120636417,-1001517843177,-1001195561278,-1001132844071,-1001908795252,-1002110566805,-1002056439885]))
@polls_extractor.on_message(filters.poll & filters.incoming)
async def start_command(client:Client,message:Message):
	chatid=[-1002056439885]
	global next
	f=""
	if message.poll.is_anonymous:
		next+=10
		if next>300:
			next=10
		next2=next
		try:
		    mess=(await polls_extractor.vote_poll(chat_id=message.chat.id, message_id=message.id,options=random.randint(0, len(message.poll.options)-1 ) ))
		    #random.randint(0, len(message.poll.options)-1 )
		except Exception as e:
		    mess=await polls_extractor.get_messages(message.chat.id,message.id)
		    mess=message.poll
			
		question=mess.question
		question=resub(question)
		
		options=[reaaa.sub("(\S*@\S*|\S*t.me\S*|\S*http\S*)","",resub(o.text)) for o in mess.options]
		correct_option_id = mess.correct_option_id
		explanation=mess.exp
		
		current=(time.localtime(time.time()+5.5*3600+next2))
		question=reaaa.sub("(\S*@\S*|\S*t\.me\S*|\S*http\S*)","",question)
		question=reaaa.sub("(^\s{1,}|^\n{1,}|\s{1,}$|\n{1,}$)","",question)
		if explanation is not None:
			explanation=reaaa.sub("(\S*@\S*|\S*t.me\S*|\S*http\S*)","",resub(explanation))
			explanation=reaaa.sub("(^\s{1,}|^\n{1,}|\s{1,}$|\n{1,}$)","",explanation)
		xy=[question,options,correct_option_id,explanation,str(f)]
		for x in chatid:
			print(str(scheduler.add_job(add_poll_to_channal, "cron",year=current.tm_year,month=current.tm_mon,day=current.tm_mday,hour=current.tm_hour, minute=current.tm_min, second=current.tm_sec,replace_existing=True,args=(x,xy,message.chat.id,message.chat.title,True,polls_extractor) ,id="job2"+id_generator()+id_generator()))[:3000])
	elif not message.from_user.is_bot:
		next+=10
		if next>300:
			next=10
		next2=next
		try:
		    mess=(await polls_extractor.vote_poll(chat_id=message.chat.id, message_id=message.id,options=random.randint(0, len(message.poll.options)-1 ) ))
		    #random.randint(0, len(message.poll.options)-1 )
		except Exception as e:
		    mess=await polls_extractor.get_messages(message.chat.id,message.id)
		    mess=message.poll
			
		question=mess.question
		question=resub(question)
		
		options=[reaaa.sub("(\S*@\S*|\S*t.me\S*|\S*http\S*)","",resub(o.text)) for o in mess.options]
		correct_option_id = mess.correct_option_id
		explanation=mess.exp
		
		current=(time.localtime(time.time()+5.5*3600+next2))
		question=reaaa.sub("(\S*@\S*|\S*t\.me\S*|\S*http\S*)","",question)
		question=reaaa.sub("(^\s{1,}|^\n{1,}|\s{1,}$|\n{1,}$)","",question)
		if explanation is not None:
			explanation=reaaa.sub("(\S*@\S*|\S*t.me\S*|\S*http\S*)","",resub(explanation))
			explanation=reaaa.sub("(^\s{1,}|^\n{1,}|\s{1,}$|\n{1,}$)","",explanation)
		xy=[question,options,correct_option_id,explanation,str(f)]
		for x in chatid:
			print(str(scheduler.add_job(add_poll_to_channal, "cron",year=current.tm_year,month=current.tm_mon,day=current.tm_mday,hour=current.tm_hour, minute=current.tm_min, second=current.tm_sec,replace_existing=True,args=(x,xy,message.chat.id,message.chat.title,False,polls_extractor) ,id="job2"+id_generator()+id_generator()))[:3000])

def add_poll_to_channal(x,y,chat,title,share,app):
	global next
	poll_topic=clientmongo["ajay"]["poll"].find_one({str(chat):{"$type":"string"}})
	if poll_topic is not None:
		topic=poll_topic[str(chat)]
	else:
		mess=app.invoke(functions.channels.CreateForumTopic(channel= app.resolve_peer(x),title=str(title),random_id=1))
		topic=str(mess.updates[0].id)
		#topic="4" 
		clientmongo["ajay"]["poll"].insert_one({str(chat):str(topic)})
	for ac in range(y[1].count("")):
		if y[1].index("")<=y[2]:
			y[2]-=1
		y[1].remove("")
	try:
		try:
			mid=app_bot.send_poll(chat_id=x,question=y[0],options=y[1],correct_option_id=y[2],reply_to_message_id=int(topic),is_anonymous=True,explanation=y[3],type=PollType.QUIZ)#reply_markup=ReplyKeyboardRemove())
		except:
			mid=app.send_poll(chat_id=x,question=y[0],options=y[1],correct_option_id=y[2],reply_to_message_id=int(topic),is_anonymous=True,explanation=y[3],type=PollType.QUIZ)#reply_markup=ReplyKeyboardRemove())
	except:
		app.send_message(x, str(y)[:3500],reply_to_message_id=int(topic))
	if chat in skip_group:
		app.invoke(
    ForwardMessages(
        from_peer= app.resolve_peer(x),
        to_peer= app.resolve_peer(x),
        id=[mid.id],
        top_msg_id=7848,
        random_id=[app.rnd_id()]
    )
)
	else:
		try:
			if share:
				if y[3] is None or y[3]=="":
					
					y[3]="join us : - @Polls_Quiz"
				if len(y[1])<10:
					y[1].append("Quiz by : - @Polls_Quiz ")
				
				try:
					app_bot.send_poll(chat_id=-1002110566805,question=y[0],options=y[1],correct_option_id=y[2],is_anonymous=False,explanation=y[3],type=PollType.QUIZ)#reply_markup=ReplyKeyboardRemove())
				except:
					app.send_poll(chat_id=-1002110566805,question=y[0],options=y[1],correct_option_id=y[2],is_anonymous=False,explanation=y[3],type=PollType.QUIZ)#reply_markup=ReplyKeyboardRemove())
			
		except:
			pass
	next-=10
	try:
		app_bot.stop_poll(x,mid.id)
	except:
		app.stop_poll(x,mid.id)
Tt={}
@app_bot.on_message(filters.regex("^force stop$")  & ~ filters.scheduled & filters.user([1604633736,6345786041,5818561062]) & filters.private )#& filters.incoming)
async def job2_partener1212(client:Client,message:Message):
	global Tt
	try:
		tim=message.text
		
		Tt[message.chat.id]["s"]=(tim)
		await app_bot.delete_messages(chat_id=message.chat.id,message_ids=message.id)
	except:
		pass
@app_bot.on_message(filters.regex("^s\.t {,}\d{1,}$")  & filters.user([1604633736,6345786041,5818561062]) & filters.private)#& filters.incoming)
async def job2_partener12(client:Client,message:Message):
	global Tt
	try:
		tim=reaaa.sub("s.t {,}","",message.text)
		
		Tt[message.chat.id]["t"]=int(tim)
		await app_bot.delete_messages(chat_id=message.chat.id,message_ids=message.id)
	except:
		await app_bot.send_message(message.chat.id, "👎")	
		

@app_bot.on_message(filters.regex("^(https://t.me/|Me/).*?/\d{1,}/\d{1,}$") & ~ filters.scheduled  & filters.user([1604633736,6345786041,5818561062]) & filters.private)#& filters.incoming)
async def job2_partener2(client:Client,message:Message):
	
        try:
            await app_bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        except:
            pass
        
        if True:
	        xx=reaaa.sub("^(https://t.me/|Me/)","",message.text)
	        xx=reaaa.sub("c/","-100",xx)
	        global Tt
	        ini=1
	        que1=""
	        tt=""
	        mmmid=[]
	        xx=reaaa.split("/",xx)
	        mess1="vote alreddy given"
	        try:
	        	xx[0]=int(xx[0])
	        except:
	        	pass
	        result={}
	        new_result = {}
	        tmarks=0
	        nn=1
	        count=1
	
	        mess4=await app_bot.invoke(functions.channels.CreateForumTopic(channel=await app_bot.resolve_peer(-1002126263044),title=reaaa.sub("^(https://t.me/|Me/)","",message.text),random_id=1))
	        reply_to_message_id=mess4.updates[0].id
		
	        
	
	        yy=None
	        
	        yy2=None
	        zzzz=0
	        #print(xx)
	        li=[x for x in range(int(xx[1]),int(xx[1])+int(xx[2]))]
	        #random.shuffle(li)
	        #await app.send_message(message.chat.id,str(li))
	        for x in li:
	    		##print(str(result))
	    
	            try:
	                if Tt[message.chat.id]["s"]=="force stop":
	                    Tt[message.chat.id]["s"]=None
	                    break
	            except:
	                pass
	            try:
	                tt1=Tt[message.chat.id]["t"]
	            except:
	                Tt[message.chat.id]={}
	                Tt[message.chat.id]["t"]=5
	                tt1=30
	            try:
	            	try:
		            	try:
		            		mess1=(await polls_extractor.vote_poll(chat_id=xx[0], message_id=x,options=1))
		            	except Exception as e:
		            		mess1=(await polls_extractor.get_messages(xx[0],x))
		            		mess1=mess1.poll
	            	except Exception as e:
		            	try:
		            		mess1=(await app.vote_poll(chat_id=xx[0], message_id=x,options=1))
		            	except Exception as e:
		            		mess1=(await app.get_messages(xx[0],x))
		            		mess1=mess1.poll
	            	
	            	
	
	            	off_set=None
	            	question=mess1.question
	            	explanation=mess1.exp
	            	
	            	if explanation is not None and explanation!="":
	            	    explanation=reaaa.sub(r"(http|ftp|https|t\.me|tg):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", "", explanation)
	            	    explanation=reaaa.sub(r"http.*? |@.*?( |$)|t.me.*? ", "", explanation)
	            	else:
	            	    explanation="https://t.me/+79cGKW33ePQ2OTU1"
	            	#await app.send_message(message.chat.id, question)
	            	
	            	
	            	
	            	question=reaaa.sub(r"((@|#)([0-9A-Za-z\-\_\.])*(\s|\n{1,}|))|((\n| |){1,}(Join|)(\n| |)){1,}", "", question)
	            	question=reaaa.sub(r"(http|ftp|https|t\.me|tg):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", "", question)
	            	question=reaaa.sub(r"^(\[\d{1,}\/\d{1,}\] ){1,}(\d{1,}\. |\d{1,}\.)", "", question)
	            	question=reaaa.sub(r"^(\[\d{1,}\/\d{1,}\] ){1,}", "", question)
	            	question=reaaa.sub(r"^(\d{1,}\. |\d{1,}\.)(\[\d{1,}\/\d{1,}\] ){1,}", "", question)
	            	question=reaaa.sub(r"^(Q_\. |Q_\.|Q_ |Q_|Q\. |Q\.|Q |Q)(\d{1,}\. |\d{1,}\.)(\[\d{1,}\/\d{1,}\] ){1,}", "", question)
	            	question=reaaa.sub(r"^(Q_\. |Q_\.|Q_ |Q_|Q\. |Q\.|Q |Q)(\d{1,}\. |\d{1,}\.)", "", question)
	            	question=reaaa.sub(r"(\n| |){1,}(|C\.A BY)(\n| |){1,}", "", question)
	            	question=reaaa.sub(r"\n{,}(🪴:~ 🪴|⃝༺⃝꧁⃝ pragyagauri꧂⃝༻⃝)\n{,}", "", question)
	            	question=reaaa.sub(r"", "", question)
	            	options=[o.text for o in mess1.options]
	            	lis=[] 
	            	
	            	
	            	
	            	
	            	
	            	for x in range(len(options)):
	            	    options[x]=reaaa.sub("^(\[|\(|)(a|b|c|d|A|B|C|D|E|F|e|f)(\]|\)|)(\. |\.|)","",options[x])
	            	    lis.append(x)#
	            	
	            	#await app.send_message(message.chat.id,str(lis))
	            	#random.shuffle(lis)
	            	#await app.send_message(message.chat.id,str(lis))
	            	
	            	correct_option_id=mess1.correct_option_id
	            	options=[options[op] for op in lis]
	            	
	            	for o in range(len(options)):
	            	    options[o]=bytes('(\\u004'+str(o+1), 'utf-8').decode('unicode-escape')+") "+options[o]
	            	
	            	
	            	
	            
	            	
	            	mess2=(await app_bot.send_poll(chat_id=-1002126263044,question=reaaa.sub("([^\u0000-\u05C0\u2100-\u214F\u0900-\u097F\u002c\u00B2\u00B3\u00B9\u2070-\u209F\u2200-\u22FF])","",(question+"\n\nSOOJH BOOJH LIVE TEST")[:256]),options=options,correct_option_id =correct_option_id,is_anonymous=True,type=PollType.QUIZ,open_period=5,reply_to_message_id=reply_to_message_id,explanation=explanation))
	            	await asyncio.sleep(tt1)

	            except Exception as e:
	            	pass#await app_bot.send_message(message.chat.id, str(e))
def main():
	
	@st.cache_resource
	def init_connection2():
		return polls_extractor.start()
	_=init_connection2()
	polls_extractor.send_message("kinbin246","poll extract on")
	@st.cache_resource
	def init_connection2():
		return app.start()
	_=init_connection2()
	def soojh_flood_wait_start(e):
		@st.cache_resource
		def init_connection1():
			return app_bot.start()
		_=init_connection1()
		#app_bot.delete_messages("Kinbin246",f)
	try:
		@st.cache_resource
		def init_connection1():
			return app_bot.start()
		_=init_connection1()
	except FloodWait as e:
		current=(time.localtime(time.time()+5.5*3600+int(e.value)+5))
		CT=time.ctime(time.time()+5.5*3600+int(e.value)+5)
		print(scheduler.add_job(soojh_flood_wait_start, "cron",year=current.tm_year,month=current.tm_mon,day=current.tm_mday,hour=current.tm_hour, minute=current.tm_min, second=current.tm_sec,replace_existing=True,args=(int(e.value),),id="soojh_flood_wait_start"))
		
		app.send_message("kinbin246","Negative Marking Quiz is stop for "+str(e.value)+" seconds\n\nAll admin can play negative marking quiz on "+str(CT))
	idle()
	app.stop()
	
	app_bot.stop()
if __name__ == '__main__':
    main()#
