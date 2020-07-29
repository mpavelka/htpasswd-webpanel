import asab
import asab.web
from .template import Jinja2TemplateService
from .url import URLService
from .htpasswd.handler import HtpasswdHandler
from .htpasswd.service import HtpasswdService

asab.Config.add_defaults({
	"htpasswd_webpanel": {
		"secret": "",
		"basepath": "",
		"staticpath": "",
		"listen": "0.0.0.0:8080",
	}
})


class Application(asab.Application):

	def __init__(self):
		super().__init__()

		if len(asab.Config["htpasswd_webpanel"]["secret"]) < 16:
			raise RuntimeError(
				"""
				You must configure the application secret that is at least 16 characters long.
				Refer to the 'secret' key in [htpasswd_webpanel] section in ./etc/htpasswd_webpanel.conf
				"""
			)

		# Web module/service
		self.add_module(asab.web.Module)
		websvc = self.get_service('asab.WebService')

		# Web container
		self.WebContainer = asab.web.WebContainer(
			websvc,
			'htpasswd_webpanel',
			config={
				"listen": asab.Config["htpasswd_webpanel"]["listen"]
			}
		)
		URLService(self)
		Jinja2TemplateService(self)
		HtpasswdService(self)
		HtpasswdHandler(self)
