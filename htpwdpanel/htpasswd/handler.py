import aiohttp


class HtpasswdHandler(object):

	def __init__(self, app):
		self.App = app
		app.WebContainer.WebApp.router.add_get('/', self.GET_users)

	def get_template_service(self):
		return self.App.get_service("jinja2.TemplateService")

	async def GET_users(self, request):
		users = [
			{"name": "Name"}
		]
		return aiohttp.web.Response(
			text=self.get_template_service().render_template(
				request,
				"users.html",
				users=users,
			),
			content_type="text/html"
		)
