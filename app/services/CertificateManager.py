from OpenSSL import crypto
import os
import sys
import random
from app.config.CertificateManagerConfig import Config
from uuid import uuid4

class CertificateManagerService:
    def __init__(self, common_name):
        self._config = Config()
        self._key_file = self._config.ca_files_path + common_name + self._config.key_file_extension
        self._crt_file = self._config.ca_files_path + common_name + self._config.cert_file_extension
        self._common_name = common_name
        self._ca_path = self._config.ca_files_path + common_name
        self._sign_algorithm = self._config.sign_algorithm


    def create_root_ca(self, bits, validation_years):
        ca_key = crypto.PKey()
        ca_key.generate_key(crypto.TYPE_RSA, bits)

        ca_cert = crypto.X509()
        ca_cert.set_version(2)
        ca_cert.set_serial_number(int(uuid()))

        ca_subj = ca_cert.get_subject()
        ca_subj.commonName = self._common_name

        ca_cert.add_extensions([
            crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=ca_cert),
        ])

        ca_cert.add_extensions([
            crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always,issuer:always', issuer=ca_cert),
            crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
            crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')
        ])
        ca_cert.set_issuer(ca_subj)
        ca_cert.set_pubkey(ca_key)
        ca_cert.sign(ca_key, self._sign_algorithm)

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(validation_years*365*24*60*60)

        
        self._save_cert_in_file_system(ca_cert)
        self._save_key_in_file_system(ca_key)

    def _save_cert_in_file_system(self, cert):
        with open(self._crt_file, "wt") as file:
            cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('ascii')
            file.write(cert_str)

    def _save_key_in_file_system(self, key):
        with open(self._key_file, "wt") as file:
            key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('ascii')
            file.write(key_str)

    def _check_root_path_exist(self, ca_path):
        if os.path.isdir(ca_path):
            return True

    def _create_root_path(self, ca_folder):
        os.mkdir(ca_folder, 700)

    def check_ca_exists(self):
        if not self._check_root_path_exist(self._config.ca_files_path):
            self._create_root_path(self._config.ca_files_path)

        if os.path.isfile(self._key_file) and os.path.isfile(self._crt_file):
            return True

    def create_intermediate_ca(self, common_name, bits, issuer):
        intermediate_key = PKey()
        intermediate_key.generate_key(TYPE_RSA, bits)
        intermediate_cert = X509()
        intermediate_cert.get_subject().commonName = common_name
        intermediate_cert.set_issuer(cacert.get_subject())
        intermediate_cert.set_pubkey(ikey)
        intermediate_cert.gmtime_adj_notBefore(0)
        intermediate_cert.gmtime_adj_notAfter(2*365*24*60*60)
        intermediate_cert.add_extensions([caext])
        intermediate_cert.set_serial_number(0)
        intermediate_cert.sign(cakey, self._sign_algorithm)
