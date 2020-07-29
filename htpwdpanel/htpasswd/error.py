class HtpasswdError(Exception):
	pass


class FileIdNotFound(HtpasswdError):
	pass


class FileNotFound(HtpasswdError):
	pass


class InvalidFile(HtpasswdError):
	pass


class UserNotFound(HtpasswdError):
	pass
