class Config:
	def __init__(self):
		self._ca_files_path = '/app/CA_files/'
		self._cert_file_extension = '.crt'
		self._key_file_extension = '.key'
		self._sign_algorithm = "sha256"

	@property
	def cert_file_extension(self):
		return self._cert_file_extension

	@property
	def key_file_extension(self):
		return self._key_file_extension
	
	@property
	def ca_files_path(self):
		return self._ca_files_path
	
	@property
	def sign_algorithm(self):
		return self._sign_algorithm
	