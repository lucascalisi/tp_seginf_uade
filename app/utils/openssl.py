from OpenSSL import crypto



class OpenSSLService:
	def __init__(self, sign_algorithm):
        self._sign_algorithm = sign_algorithm

	def create_private_key(self, type_key, bits)
		try:
			key = crypto.PKey()
        	key.generate_key(type_key, bits)
		except Exception as e:
			raise e

        return key

    def create_certificate(self, version, serial_number, X509_subject, valid_for_years, key)
        ca_cert = crypto.X509()
        ca_cert.set_version(version)
        ca_cert.set_serial_number(serial_number)

        ca_subj = ca_cert.get_subject()
        ca_subj.commonName = X509_subject.common_name
        ca_subj.organizationalUnitName = X509_subject.organizational_unit_name
        ca_subj.organizationName = X509_subject.organization_name
        ca_subj.localityName = X509_subject.locality_name
        ca_subj.stateOrProvinceName = X509_subject.state_or_province_name
        ca_subj.countryName = X509_subject.country_name

        if X509_extensions:
        ca_cert.add_extensions(X509_extensions)

        ca_cert.set_issuer(ca_subj)
        ca_cert.set_pubkey(key)

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(valid_for_years*365*24*60*60)

        return ca_cert

	def sign_certificate(self, ca_cert, ca_key, sign_algorithm)
        ca_cert.sign(ca_key, sign_algorithm)
        return ca_cert

    def dump_certificate_to_ascii(self, cert):
        return crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('ascii')

    def dump_privatekey_to_ascii(self, key)
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('ascii')

    def set_extensions_to_ca(self, cert):
        cert.add_extensions([
            crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=cert),
        ])

        cert.add_extensions([
            crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always,issuer:always', issuer=cert),
            crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
            crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')
        ])

    def set_extensions_to_server_cert(self, cert):
        cert.add_extensions([
        X509Extension(b'basicConstraints', True, b'CA:false')])