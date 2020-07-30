import asab
import aiohttp
import datetime
import logging
import jwt
from .error import HtpasswdError


L = logging.getLogger(__name__)


class HtpasswdHandler(object):

	def __init__(self, app):
		self.App = app
		self.TemplateService = app.get_service("jinja2.TemplateService")
		self.HtpasswdService = app.get_service("htpasswd_webpanel.HtpasswdService")
		app.WebContainer.WebApp.router.add_get('/', self.GET_users)
		app.WebContainer.WebApp.router.add_post('/delete', self.POST_delete_user)
		app.WebContainer.WebApp.router.add_get('/token', self.GET_token)
		app.WebContainer.WebApp.router.add_get('/public/register', self.GET_register)
		app.WebContainer.WebApp.router.add_post('/public/register', self.POST_register)

	async def GET_users(self, request):
		try:
			users = self.HtpasswdService.read_users("default")
		except HtpasswdError:
			users = None

		return aiohttp.web.Response(
			text=self.TemplateService.render_template(
				request,
				"users.html",
				users=users,
			),
			content_type="text/html"
		)

	async def POST_delete_user(self, request):
		form = await request.post()
		user = form.get("user")

		if user is None:
			L.error("'user' is missing in the form data")
			raise aiohttp.web.HTTPBadRequest()

		if not self.HtpasswdService.validate_user_name(user):
			L.error("Invalid user name provided in 'user' key.")
			raise aiohttp.web.HTTPBadRequest()

		try:
			self.HtpasswdService.delete_user(user)
		except HtpasswdError as e:
			L.error("Can't delete user. {}".format(e))
			raise aiohttp.web.HTTPBadRequest()

		return aiohttp.web.HTTPFound(location="./")

	async def POST_register(self, request):

		try:
			form = await request.post()
			token = form["token"]
			password = form["password"]
		except KeyError as e:
			L.error("Missing key '{}'".format(e))
			raise aiohttp.web.HTTPBadRequest()

		try:
			jwt_data = jwt.decode(
				token,
				asab.Config["htpasswd_webpanel"]["secret"],
				verify=True
			)
			user = jwt_data["user"]
		except jwt.exceptions.InvalidTokenError:
			return await self._respond_invalid_token(request)
		except KeyError:
			return await self._respond_invalid_token(request)

		if not self.HtpasswdService.validate_user_name(user):
			L.error("Invalid user name provided in 'user' key.")
			return await self._respond_invalid_token(request)

		try:
			self.HtpasswdService.add_user(user, password)
		except HtpasswdError as e:
			L.error("Can't add user. {}".format(e))
			raise aiohttp.web.HTTPBadRequest()

		return aiohttp.web.Response(
			text="Success!",
			content_type="text/html"
		)

	async def GET_register(self, request):
		token = request.query.get("token")
		if token is None:
			return await self._respond_invalid_token(request)

		try:
			jwt_data = jwt.decode(
				token,
				asab.Config["htpasswd_webpanel"]["secret"],
				verify=True
			)
		except jwt.exceptions.InvalidTokenError:
			return await self._respond_invalid_token(request)

		try:
			user = jwt_data["user"]
		except KeyError:
			return await self._respond_invalid_token(request)

		return aiohttp.web.Response(
			text=self.TemplateService.render_template(
				request,
				"register.html",
				user=user,
				token=token,
			),
			content_type="text/html"
		)

	async def GET_token(self, request):
		user = request.query.get("user")
		if user is None:
			L.error("'user' is missing in the query")
			return aiohttp.web.Response(
				text="URL query does not contain 'user'",
				content_type="text/html"
			)

		if not self.HtpasswdService.validate_user_name(user):
			L.error("Invalid user name provided in 'user' key.")
			return aiohttp.web.Response(
				text="Invalid user name...",
				content_type="text/html"
			)

		token = jwt.encode(
			{
				'user': user,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
			},
			asab.Config["htpasswd_webpanel"]["secret"],
		)

		return aiohttp.web.Response(
			text=self.TemplateService.render_template(
				request,
				"token.html",
				token=token.decode()
			),
			content_type="text/html"
		)

	async def _respond_invalid_token(self, request):
		return aiohttp.web.Response(
			text=self.TemplateService.render_template(
				request,
				"invalid_token.html"
			),
			content_type="text/html"
		)

