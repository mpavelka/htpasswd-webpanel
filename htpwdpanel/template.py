import asab
import jinja2


class Jinja2TemplateService(asab.Service):
	def __init__(self, app):
		super().__init__(app, service_name="jinja2.TemplateService")

		self.Loader = jinja2.FileSystemLoader("templates")
		self.Environment = jinja2.Environment(
			loader=self.Loader,
			autoescape=jinja2.select_autoescape(['html', 'xml'])
		)

	async def initialize(self, app):
		self.Environment.globals.update()

	def render_template(
			self,
			request,
			template_name,
			**kwargs
	):
		"""
		Renders template using Jinja2

		**kwargs will be passed to the template as template variables.
		"""
		template = self.Environment.get_template(template_name)

		# Render!
		return template.render(
			Request=request,
			**kwargs
		)
