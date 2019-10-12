import os

class Config:
	def __init__(self):
		self.app_path = os.environ["PATH_APP_CA_FILES"]
		self.sign_algorithm = "sha256"
		self.root_authority_conf = {
			"bit_size" : 2048,
			"valid_years" : 20,
			"name" : "PRUEBA_CA"
		}
