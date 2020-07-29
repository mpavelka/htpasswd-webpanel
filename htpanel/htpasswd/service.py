import asab
import htpasswd
import logging
import re
from .error import (
	FileIdNotFound,
	FileNotFound,
	InvalidFile,
	UserNotFound
)

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
	RE_USER_NAME = re.compile(r'^[A-Za-z0-9-_]{1,256}$')

	def __init__(self, app):
		super().__init__(app, service_name="htpasswd_webpanel.HtpasswdService")

	def read_users(self, file_id="default"):
		path = self._get_file_path(file_id)
		if path is None:
			raise FileIdNotFound()

		try:
			with htpasswd.Basic(path) as userdb:
				users = userdb.users
		except FileNotFoundError:
			L.error("File '{}' not found.".format(path))
			raise FileNotFound()
		except ValueError as e:
			L.error("Invalid file '{}': {}".format(path, e))
			raise InvalidFile()

		return users

	def delete_user(self, user, file_id="default"):
		path = self._get_file_path(file_id)
		if path is None:
			raise FileIdNotFound()

		try:
			with htpasswd.Basic(path) as userdb:
				userdb.pop(user)
		except FileNotFoundError:
			L.error("File '{}' not found.".format(path))
			raise FileNotFound()
		except ValueError as e:
			L.error("Invalid file '{}': {}".format(path, e))
			raise InvalidFile()
		except htpasswd.basic.UserNotExists:
			L.error("User '{}' doesn't exist".format(user))
			raise UserNotFound()

	def add_user(self, user, password, file_id="default"):
		path = self._get_file_path(file_id)
		if path is None:
			raise FileIdNotFound()

		try:
			with htpasswd.Basic(path) as userdb:
				userdb.add(user, password)
		except FileNotFoundError:
			L.error("File '{}' not found.".format(path))
			raise FileNotFound()
		except ValueError as e:
			L.error("Invalid file '{}': {}".format(path, e))
			raise InvalidFile()
		except htpasswd.basic.UserExists:
			L.error("User '{}' already exists".format(user))
			raise UserNotFound()

	def validate_user_name(self, user_name):
		return self.RE_USER_NAME.match(user_name) is not None

	def _get_file_path(self, file_id):
		config_section = self._get_file_config_section(file_id)
		return config_section.get("path") if config_section is not None else None

	def _get_file_config_section(self, file_id):
		try:
			return asab.Config["htpasswd_file:{}".format(file_id)]
		except KeyError:
			L.warn("No such file_id {}".format(file_id))
			return None
