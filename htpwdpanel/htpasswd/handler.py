import aiohttp


class HtpasswdHandler(object):

	def __init__(self, app):
		self.App = app
		self.TemplateService = app.get_service("jinja2.TemplateService")
		self.HtpasswdService = app.get_service("htpasswd_webpanel.HtpasswdService")
		app.WebContainer.WebApp.router.add_get('/', self.GET_users)

	async def GET_users(self, request):
		return aiohttp.web.Response(
			text=self.TemplateService.render_template(
				request,
				"users.html",
				users=self.HtpasswdService.read_users("default"),
			),
			content_type="text/html"
		)
