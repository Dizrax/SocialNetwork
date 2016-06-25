from models import Session, User, Photo, Friendship, Friendrequest, Base, engine, DBSession


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

user1 = User(name = "Ann", lastname ="Smith",login='An', password ='123',city='Ekb', age=20,avatar = 'http://localhost:6543/static/An.jpg')
user2 = User(name = "Sarah", lastname ="Bet",login='SB', password ='000',city='New York', age=17,avatar = 'http://localhost:6543/static/SB.jpg')
user3 = User(name = "John", lastname ="Worf",login='JJ', password ='90',city='London', age=21,avatar = 'http://localhost:6543/static/JJ.jpg')

photo1 = Photo(user_id = 1, path = 'http://localhost:6543/static/9.jpg')
photo2 = Photo(user_id = 1, path = 'http://localhost:6543/static/10.jpg')
photo3 = Photo(user_id = 2, path = 'http://localhost:6543/static/11.jpg')

fr = Friendrequest(user_from_id = 1, user_to_id = 3)

fs1 = Friendship(user_from_id = 1, user_to_id = 2, dialogLocPath = 'socialnetwork/static/2-1.txt',dialogPath ='http://localhost:6543/static/2-1.txt')
fs2 = Friendship(user_from_id = 2, user_to_id = 3, dialogLocPath = 'socialnetwork/static/2-3.txt',dialogPath ='http://localhost:6543/static/2-3.txt')

DBSession.add_all([user1,user2,user3,photo1,photo2,photo3,fr,fs1,fs2])
#print(DBSession.query(User).all())
