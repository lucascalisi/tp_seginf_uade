# TPO UADE - PKI API
API para generar Certificate Authority interna para gestionar la firma y renovacion de certificados digitales para tus aplicaciones.

## Integrantes:
  * Calisi, Lucas Pablo 
  * Alonso, Juan Cruz

#### Como corro la app?

git clone https://github.com/lucascalisi/tp_seginf_uade.git <br/>
cd tp_seginf_uade <br/>

#### Linux Environments
chmod o+rx docker-run.sh <br/>

#### Windows Environments
docker build -t pki-api .
OS_PERSISTENCE_PATH= PATH FISICO PARA OBTENER PERSISTENCIA EN EL HOST
APP_PATH= PATH EN LA APP

docker run -v %OS_PERSISTENCE_PATH%:%APP_PATH% -it -p 8080:8080 pki-api


#### Que puedo hacer con esta API?

* Podemos generar una CA interna para nuestra empresa y firmar certificados digitales para nuestras aplicaciones de manera rapida. La CA ROOT se genera automaticamente al iniciar la APP, o si ya fue generada la levanta del filesystem. El common name de la CA debe estar configurado en el archivo de configuracion.

Authorizar a una CA Intermedia a firmar certificados
  * /api/v1/certificate_manager/intermediate/create
  * POST
  * JSON
```javascript
{
	"IntermediateCertificateAuthority" : {
		"Name" : "INTER_CA",
		"Bits" : 2048,
		"ValidFor" : 10
	}
}
```

Generar Certificados para servidores firmados con una entidad intermedia
  * /api/v1/certificate_manager/server/create
  * POST
  * JSON
```javascript
{
	"Certificate" : {
		"Name" : "PRUEBA_LUCAS",
		"Bits" : 2048,
		"ValidFor" : 1,
		"Signer" : "INTER_CA"
	}
}
```


