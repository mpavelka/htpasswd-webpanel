import asab
import htpasswd
import logging

###

L = logging.getLogger(__name__)

###

asab.Config.add_defaults({
	"htpasswd_file:default": {
		"path": "/etc/apache2/.htpasswd"
	}
})

###


class HtpasswdService(asab.Service):

	def __init__(self, app):
		super().__init__(app, service_name="htpasswd_webpanel.HtpasswdService")

	def read_users(self, file_id="default"):
		path = self._get_file_path(file_id)
		if path is None:
			return None

		try:
			with htpasswd.Basic(path) as userdb:
				users = userdb.users
		except FileNotFoundError:
			L.error("File '{}' not found.".format(path))
			return None

		return users

	def _get_file_path(self, file_id):
		config_section = self._get_file_config_section(file_id)
		return config_section.get("path") if config_section is not None else None

	def _get_file_config_section(self, file_id):
		try:
			return asab.Config["htpasswd_file:{}".format(file_id)]
		except KeyError:
			L.warn("No such file_id {}".format(file_id))
			return None
