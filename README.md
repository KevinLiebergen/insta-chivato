# Who doesn't follow me back on Instagram?

Prueba de concepto para entender como interactuar con Instagram debido a la actualización de la nueva API v2.0, que sólo te permite interactuar si eres un [negocio o una cuenta profesional](https://developers.facebook.com/docs/instagram-api)

La API básica de la v2.0 solo te permite realizar [ciertos métodos](https://developers.facebook.com/docs/instagram-basic-display-api/reference/user)


Debido a esto interactuamos directamente como si fuéramos un navegador, sin API y con cookies y CSRF, necesario deshabilitar segundo factor de autenticación.

Login basado en [instagram-scraper](https://github.com/rarcega/instagram-scraper/tree/0d064613d8ca033700d31a7ec1c7ae4a90cb3bc8)

### Utilización

#### Método 1
Sustituir `user` y `password` por sus credenciales, mantener las comillas simples.
<br>`$ python3 insta-scra.py -u='user' -p='password'`

#### Método 2
Tambien puede crear un fichero `insta_args.txt` con el siguiente contenido:
```
-u=usuario
-p=password
```

Y ejecutar el siguiente comando:
<br>`$ python3 insta-scra.py @insta_args.txt`

Ver información acerca de una cuenta ajena (la cuenta sin el símbolo arroba)
<br>`$ python3 insta-scra.py @insta_args.txt <user>`

