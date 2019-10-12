class IntermediateCertificateNotFound(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class IntermediateCertificateAlreadyExists(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class GetRootCertificateAuthorityError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class CreateRootCertificateError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class LoadCertificateFromFileSystemError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class SaveCertificateInFileSystemError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc

class CreateFolderError(Exception):
	def __init__(self, error_desc):
		self.error_desc = error_desc	