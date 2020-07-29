import asab


class URLService(asab.Service):

	def __init__(self, app):
		super().__init__(app, service_name="htpasswd_webpanel.URLService")
		self.BasePath = asab.Config["htpasswd_webpanel"]["basepath"]
		self.StaticPath = asab.Config["htpasswd_webpanel"]["staticpath"]

	def gen_url(
			self,
			request,
			path,
			query={},
			external=False,
			static=False
	):
		# TODO: base path
		x_forwarded_proto = request.headers.get("X-Forwarded-Proto")
		x_forwarded_for = request.headers.get("X-Forwarded-For")
		scheme = request.scheme
		host = request.host

		query_string = ""
		if len(query) > 0:
			amp = False
			query_string = "?"

			for key, value in query.items():
				if amp:
					query_string += "&"
				else:
					amp = True
				query_string += "{}={}".format(key, value)

		url = ""
		if external:
			url += "{}://{}".format(
				x_forwarded_proto if x_forwarded_proto is not None else scheme,
				x_forwarded_for if x_forwarded_for is not None else host,
			)

		url += "{}{}{}".format(
			self.BasePath if not static else self.StaticPath,
			path,
			query_string
		)

		return url
