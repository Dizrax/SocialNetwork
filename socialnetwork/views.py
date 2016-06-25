# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from sqlalchemy import create_engine
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import forget, remember,authenticated_userid
import cgi
import os
import datetime
import urlparse
from models import  User, Photo, Friendship, Friendrequest, engine, Session 
from sqlalchemy import and_,or_
#e = create_engine("sqlite:///sndb.db")

@view_config(route_name='entry', renderer = 'templates/entry.pt')
def entry_view(request):	
	return {"visibility":"hidden",'text' : u""}
	

@view_config(route_name='registration', renderer = 'templates/registration.pt')
def registration_view(request):			
	if (request.method == "POST"):	
		name = request.params['name']
		lastname = request.params['lastname']
		login = request.params['login']
		password = request.params['password']
		if(name != '' and lastname != '' and login != '' and password != ''):			
			DBSession = Session(bind=engine)
			users = DBSession.query(User).filter(User.login == login).all()
			if(len(users) == 0):
				avatar = request.static_url('socialnetwork:static/defaultAvatar.png') 				
				user = User(name = name, lastname = lastname,login = login, password = password,avatar = avatar)
				DBSession.add(user)
				DBSession.commit()
				return {'visibility':'visible', 'text' : u"Успешная регистрация!"}	
			else: return {'visibility':'visible', 'text' : u"Такой логин уже занят"}		
		else: return {'visibility':'visible', 'text' : u"Не все поля заполнены"}		
	return {'visibility':'hidden', 'text': ''}

@view_config(route_name='login', renderer = 'templates/entry.pt')
def login(request):	
	login = authenticated_userid(request)
	if(login!= None):
    		return HTTPFound(location='logout')	
	login,password = '',''
	if (request.method == "POST"):
		login = request.params['login']
		password = request.params['password']
		if(login != '' and password != ''):			
			DBSession = Session(bind=engine)
		
			print(DBSession.query(User).all())
			user = DBSession.query(User).filter(and_(User.login == login, User.password == password)).all()		
			if(len(user)>0): 
				headers = remember(request, login)					
				return HTTPFound(location='/myprofile', headers=headers)
					
	return {"visibility":"visible",'text' : u"Неверный логин или пароль"}



@view_config(route_name='myprofile', renderer = 'templates/myprofile.pt')
def myprofile_view(request):	
	login = authenticated_userid(request)
	if(login!= None):
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()			
		return {'name':user.name,'lastname':user.lastname,'city':user.city,\
			'age':user.age, 'avatar':user.avatar, 'visibility':['hidden','hidden','hidden','hidden']}	
	
	return HTTPFound(location='/')


@view_config(route_name='editProfile', renderer = 'templates/editProfile.pt')
def editProfile_view(request):	
	login = authenticated_userid(request)
	if(login!= None):
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()		 
		return {'name':user.name,'lastname':user.lastname,'city':user.city,\
			'age':user.age, 'avatar':user.avatar}	
	
	return HTTPFound(location='/')


@view_config(route_name='edit')
def edit_view(request):
	login = authenticated_userid(request)		
	if(login!= None):
		imageName  = login+'Avatar'
		with open("socialnetwork/static/"+imageName,'wb') as f:
			f.write(request.params["myimg"].value)
		name = request.params["name"]
		lastname = request.params["lastname"]
		city = request.params["city"]
		age = request.params["age"]
		avatar = request.static_url('socialnetwork:static/'+imageName)

		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()

		user.name = name
		user.lastname = lastname
		user.city = city
		user.age = age
		user.avatar = avatar
		DBSession.commit()		
				
		return HTTPFound(location='myprofile')	
	return HTTPFound(location='/')

@view_config(route_name='friends', renderer = 'templates/friends.pt')
def friends_view(request):
	login = authenticated_userid(request)	
	if(login!= None):
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()	
		print(user.children)		
		
		fs1 = 	DBSession.query(Friendship.user_from_id).filter(Friendship.user_to_id==user.id)
		fs2 = 	DBSession.query(Friendship.user_to_id).filter(Friendship.user_from_id==user.id)	
		friends = DBSession.query(User.name,User.lastname,User.avatar,User.id).filter(or_(User.id.in_(fs1),User.id.in_(fs2)))

		userIds = DBSession.query(Friendrequest.user_from_id).filter(Friendrequest.user_to_id == user.id)
		requests = DBSession.query(User.name,User.lastname,User.avatar,User.id).filter(User.id.in_(userIds)) 		
		
		return {'friends':friends,'requests':requests}
	return HTTPFound(location='/')

@view_config(route_name='profile', renderer = 'templates/myprofile.pt')
def profile_view(request):
	login = authenticated_userid(request)	
	if(login!= None):
		friendId = int(request.query_string.split('=')[1])
		DBSession = Session(bind=engine)
		friend = DBSession.query(User).filter(User.id == friendId).one()
		user = DBSession.query(User).filter(User.login == login).one()		
		
		#скрытие кнопок
		add,delete,photo,message = '','','',''
		#если это мой акк		
		if (user.id == friendId): add,delete,photo,message = 'hidden','hidden','hidden','hidden'
		else:	
				
			friendships = DBSession.query(Friendship).filter(or_(and_(Friendship.user_to_id==user.id, Friendship.user_from_id==friendId),and_(Friendship.user_to_id==friendId, Friendship.user_from_id==user.id))).all()			
			print(friendships[0].user_from)
			#для незнакомого
			if(len(friendships) == 0):add,delete,photo,message = '','hidden','hidden','hidden'

			#если это мой друг
			else : 	add,delete,photo,message = 'hidden','','',''
			 
		return {'name':friend.name,'lastname':friend.lastname,'city':friend.city,\
			'age':friend.age, 'avatar':friend.avatar,'visibility':[add, delete, photo, message]}
	return HTTPFound(location='/')	    	

@view_config(route_name='photo', renderer = 'templates/photo.pt')
def photo_view(request):
	login = authenticated_userid(request)	
	if(login!= None):
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()
			
		photos = []
		for photo in user.photos:
			photos.append(photo.path)			
		return {'photos':photos, 'visibility' : 'visible'}
    	return HTTPFound(location='/')

@view_config(route_name='loadPhoto', renderer = 'templates/photo.pt')
def loadPhoto_view(request):
	login = authenticated_userid(request)		
	if(login!= None):
		
		imageName  = login+'Photo'+ str(datetime.datetime.now())
		with open("socialnetwork/static/"+imageName,'wb') as f:
			f.write(request.params["myimg"].value)
		path = request.static_url('socialnetwork:static/'+imageName)	

		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()	
		photo = Photo(user_id = user.id, path = path)
		DBSession.add(photo)
		DBSession.commit()
		
		return HTTPFound(location='/photo')	
	return HTTPFound(location='/')

@view_config(route_name='search', renderer = 'templates/search.pt')
def search_view(request):
	login = authenticated_userid(request)		
	if(login!= None):		
		name = request.params['name']
		lastname = request.params['lastname']
		age = request.params['age']
		city = request.params['city']
		
		DBSession = Session(bind=engine)
		result = DBSession.query(User.name, User.lastname, User.avatar,User.id).filter(User.login != login)	
		if(name != ''): result = result.filter(User.name == name)
		if(lastname != ''): result = result.filter(User.lastname == lastname)
		if(age != ''): result = result.filter(User.age == age)
		if(city != ''): result = result.filter(User.city == city)			
		return {'dictionary':result.all()}
    	return HTTPFound(location='/')

@view_config(route_name='makefriend')
def makefriend(request):
	login = authenticated_userid(request)		
	if(login!= None):
		parsed = urlparse.urlparse(request.referer)
		friendid = int(urlparse.parse_qs(parsed.query)['id'][0])
		
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()

		friendrequest = DBSession.query(Friendrequest).filter(and_(Friendrequest.user_to_id == user.id,Friendrequest.user_from_id == friendid)).all()
			
		#принимаем заявку в друзья
		if (len(friendrequest) > 0):							

			messageFile = "{0}-{1}.txt".format(user.id, friendid)
			messageLocPath =  "socialnetwork/static/" +messageFile
			with open(messageLocPath,'w') as f:
				f.write('')
			
			friendship = Friendship(user_from_id = friendid, user_to_id = user.id, dialogLocPath = messageLocPath)
			DBSession.add(friendship)				
			DBSession.delete(friendrequest[0])
			DBSession.commit()			
		
		else:	
			#запрос от текущего аккаунта выбранному пользователю			
			friendrequest = DBSession.query(Friendrequest).filter(and_(Friendrequest.user_to_id == friendid,Friendrequest.user_from_id == user.id)).all()				
			#добавление, если нет еще запроса
			if (len(friendrequest) == 0 ):
				friendrequest = Friendrequest(user_from_id = user.id, user_to_id = friendid)
				DBSession.add(friendrequest)	
				DBSession.commit()
		
		return HTTPFound(location=request.referer)
    	return HTTPFound(location='/')

@view_config(route_name='removefriend')
def removefriend(request):
    	login = authenticated_userid(request)		
	if(login!= None):		
		parsed = urlparse.urlparse(request.referer)
		friendId = int(urlparse.parse_qs(parsed.query)['id'][0])
		DBSession = Session(bind=engine)
		user = DBSession.query(User).filter(User.login == login).one()
		friendship = DBSession.query(Friendship).filter(or_(and_(Friendship.user_to_id==user.id, Friendship.user_from_id==friendId),and_(Friendship.user_to_id==friendId, Friendship.user_from_id==user.id))).one()
		DBSession.delete(friendship)
		DBSession.commit()	
		return HTTPFound(location=request.referer)
    	return HTTPFound(location='/')

@view_config(route_name='friendphoto', renderer = 'templates/photo.pt')
def friendphoto(request):
    	login = authenticated_userid(request)		
	if(login!= None):		
		parsed = urlparse.urlparse(request.referer)
		friendid = int(urlparse.parse_qs(parsed.query)['id'][0])

		DBSession = Session(bind=engine)	
		friend = DBSession.query(User).filter(User.login == login).one()
			
		photos = []
		for photo in friend.photos:
			photos.append(photo.path)			
				
		return {'photos':photos, 'visibility' : 'hidden'}
    	return HTTPFound(location='/')

@view_config(route_name='message', renderer = 'templates/messages.pt')
def messages(request):
    	login = authenticated_userid(request)		
	if(login!= None):		
		parsed = urlparse.urlparse(request.referer)
		friendid = []
		try: friendid = int(urlparse.parse_qs(parsed.query)['id'][0])
		except : friendid = int(request.query_string.split('=')[1])

		DBSession = Session(bind=engine)	
		currentUser = DBSession.query(User).filter(User.login == login).one()			
		fs = DBSession.query(Friendship).filter(or_\
							(and_(Friendship.user_from_id == friendid, Friendship.user_to_id == currentUser.id),\
							 and_(Friendship.user_from_id == currentUser.id, Friendship.user_to_id == friendid))).one()			
		lines = []
		if (not os.path.exists(fs.dialogLocPath)):
			f = open(messageLocPath,'w') 
			f.write('')								
			f.close()
		with open(fs.dialogLocPath,'r') as f:
			for line in f:
				lines.append(line)
		lenght = len(lines)
		if( lenght > 10):
			lines = lines[lenght -10:lenght]
		return {'lines':lines, 'id':friendid}
    	return HTTPFound(location='/')

@view_config(route_name='writemessage')
def writemessage(request):
	
    	login = authenticated_userid(request)		
	if(login!= None):
		
		friendid = int(request.query_string.split('=')[1])
		
		DBSession = Session(bind=engine)
		currentUser = DBSession.query(User).filter(User.login == login).one()			

		fs = DBSession.query(Friendship).filter(or_\
							(and_(Friendship.user_from_id == friendid, Friendship.user_to_id == currentUser.id),\
							 and_(Friendship.user_from_id == currentUser.id, Friendship.user_to_id == friendid))).one()
		
		with open(fs.dialogLocPath,'a') as f:			
			f.write(currentUser.name + ' ' + currentUser.lastname+' : ' +request.params['text'].encode('ascii')+"\n")
		
		return HTTPFound(location='/message?id={}'.format(friendid))
    	return HTTPFound(location='/')


@view_config(route_name='logout')
def logout(request):
    	headers = forget(request)
    	return HTTPFound(location='/',headers=headers)

