from OpenSSL import crypto
import os
import sys
import random
from app.config.CertificateManagerConfig import Config

class CertificateManagerService:
    def __init__(self, common_name):
        self._config = Config()
        self._common_name = common_name
        self._key_file = self._config.ca_files_path + common_name + self._config.key_file_extension
        self._crt_file = self._config.ca_files_path + common_name + self._config.cert_file_extension


    def create_new_ca(self):
        ca_key = crypto.PKey()
        ca_key.generate_key(crypto.TYPE_RSA, 2048)

        ca_cert = crypto.X509()
        ca_cert.set_version(2)
        ca_cert.set_serial_number(random.randint(50000000,100000000))

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
        ca_cert.sign(ca_key, 'sha256')

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(20*365*24*60*60)

        
        self._save_cert_in_file_system(ca_cert)
        self._save_key_in_file_system(ca_key)

    def _save_cert_in_file_system(self, cert):
        with open(self._crt_file, "wt") as file:
            cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('ascii')
            file.write(cert_str)

    def _save_key_in_file_system(self, key, common_name):
        with open(self._key_file, "wt") as file:
            key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('ascii')
            file.write(key_str)

    def _check_root_path_exist(self):
        ca_path = self._config.ca_files_path + self._common_name
        if os.path.isfile(ca_path):
            return True

    def _create_root_path(self):
        print("CREO ROOT")
        os.mkdir(self._config.ca_files_path, 700)

    def check_ca_exists(self):
        if not self._check_root_path_exist():
            print("NO EXISTE")
            self._create_root_path()
        
        if os.path.isfile(self._key_file) and os.path.isfile(_crt_file):
            return True



    def sign_certificate(self):
        ###############
        # Client Cert #
        ###############

        client_key = crypto.PKey()
        client_key.generate_key(crypto.TYPE_RSA, 2048)

        client_cert = crypto.X509()
        client_cert.set_version(2)
        client_cert.set_serial_number(random.randint(50000000,100000000))

        client_subj = client_cert.get_subject()
        client_subj.commonName = "Client"

        client_cert.add_extensions([
            crypto.X509Extension("basicConstraints", False, "CA:FALSE"),
            crypto.X509Extension("subjectKeyIdentifier", False, "hash", subject=client_cert),
        ])

        client_cert.add_extensions([
            crypto.X509Extension("authorityKeyIdentifier", False, "keyid:always", issuer=ca_cert),
            crypto.X509Extension("extendedKeyUsage", False, "clientAuth"),
            crypto.X509Extension("keyUsage", False, "digitalSignature"),
        ])

        client_cert.set_issuer(ca_subj)
        client_cert.set_pubkey(client_key)
        client_cert.sign(ca_key, 'sha256')

        client_cert.gmtime_adj_notBefore(0)
        client_cert.gmtime_adj_notAfter(10*365*24*60*60)

        # Save certificate
        with open("client.crt", "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert))

        # Save private key
        with open("client.key", "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client_key))
#if __name__ == "__main__":
#    ca_manager = CertificateManagerService('HSBC')
#    ca_manager.create_new_ca()