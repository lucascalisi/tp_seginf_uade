# TPO UADE - PKI API
API para generar Certificate Authority interna para gestionar la firma y renovacion de certificados digitales para tus aplicaciones.

## Integrantes:
  * Calisi, Lucas Pablo 
  * Alonso, Juan Cruz
  * Fernandez, Gonzalo Ariel




#### Como corro la app?

git clone https://github.com/lucascalisi/tp_seginf_uade.git <br/>
cd tp_seginf_uade <br/>
chmod o+rx docker-run.sh <br/>
./docker-run.sh <br/>


#### Que puedo hacer con esta API?

* Podemos generar una CA interna para nuestra empresa y firmar certificados digitales para nuestras aplicaciones de manera rapida
  * /api/v1/ca_manager/create <br>
  * POST
  * JSON
```javascript
{
	"CertificateAuthority": {
		"Name" : "CA_NAME",
		"Bits" : 2048,
		"ValidFor" : 20
	}
}
```
