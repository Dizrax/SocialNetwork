from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.view import view_config

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
    	"""

    	config = Configurator(settings=settings)

	authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)

    	config.include('pyramid_chameleon')

    	config.add_static_view(name='static', path='socialnetwork:static')

    	config.add_route('entry', '/')
	config.add_route('registration', '/registration')
	config.add_route('myprofile', '/myprofile')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')	    	
	config.add_route('editProfile', '/editProfile')	
	config.add_route('edit', '/edit')
	
	config.add_route('friends', '/friends')
	config.add_route('photo', '/photo')
	config.add_route('loadPhoto', '/loadPhoto')
	config.add_route('profile', '/profile')
	config.add_route('search', '/search')
	config.add_route('makefriend', '/makefriend')	
	config.add_route('removefriend', '/removefriend')
	config.add_route('friendphoto', '/friendphoto')
	config.add_route('message', '/message')
	config.add_route('writemessage', '/writemessage')
	config.scan()

    	return config.make_wsgi_app()


