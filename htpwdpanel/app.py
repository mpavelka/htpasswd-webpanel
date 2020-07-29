import asab
import asab.web
from .template import Jinja2TemplateService
from .htpasswd.handler import HtpasswdHandler

asab.Config.add_defaults({
	"htpasswd_webpanel": {
		"listen": "0.0.0.0:8080"
	}
})


class Application(asab.Application):

	def __init__(self):
		super().__init__()

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

		Jinja2TemplateService(self)

		# HtpasswdService(self)
		HtpasswdHandler(self)
