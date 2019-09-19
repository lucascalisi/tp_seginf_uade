class ParseRequestError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc