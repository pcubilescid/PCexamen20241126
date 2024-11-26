from http.server import HTTPServer , BaseHTTPRequestHandler
import urllib.parse

# HTML para el formulario que permite ingresar base y altura
html_calc_triangulo = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculador de Área de Triángulos PC</title>
    </head>
    <body>
        <h1>Calculador de Área de Triángulos PC</h1>

        <form action="/calcular_area" method="POST"> <label for="base">Base:</label>
            <input type="number" id="base" name="base" required>

            <label for="altura">Altura:</label>
            <input type="number" id="altura" name="altura" required>

            <button type="submit">Calcular</button>
        </form>
    </body>
    </html>
"""

def genera_resultado(base, altura):
    """
    Genera una página HTML con el resultado del cálculo del área de un triángulo.

    Args:
        base (float): La base del triángulo.
        altura (float): La altura del triángulo.

    Returns:
        str: Código HTML que muestra el resultado del cálculo.
    """
    resultado = base * altura/2
    html_area= f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculador de Área de Triángulos</title>
    </head>
    <body>
        <h1>Calculador de Área de Triángulos</h1>

        <h3>El área de un triángulo de base {base} y altura {altura} es: {resultado}</h3>
    </body>
    </html>
    """
    return html_area

class LMCDPRequestHandler(BaseHTTPRequestHandler):
    """
    Manejador de solicitudes HTTP para servir el formulario de cálculo de áreas
    y procesar el cálculo de áreas de triángulos.
    """
    
    def do_GET(self):
        """
        Maneja las solicitudes GET enviando el formulario HTML al cliente.
        
        self: Representa la instancia actual del manejador que procesa
        la solicitud. A través de self accedemos a atributos y métodos
        que definen el comportamiento de esta solicitud específica.

        Este método se ejecuta cuando el servidor recibe una solicitud GET del cliente 
        (como cuando un usuario accede al servidor desde un navegador).

        Escribe el contenido del formulario HTML ('html_calc_triangulo') en el cuerpo de la 
        respuesta, codificado en UTF-8. Este formulario permite al usuario ingresar los valores 
        de base y altura de un triángulo para calcular su área.

        Entrega al cliente un formulario HTML que puede ser utilizado para 
        enviar datos al servidor mediante una solicitud POST.
        """
        # Imprimimos detalles del objeto self para depurar y entender el estado
        print("------- Contenido del request SELF-------")
        print(f"path = {self.path}") # Ruta solicitada por el cliente
        for key, value in self.__dict__.items(): # Atributos de la instancia
            print (f"Atributo de instancia ='{key}' contiene {value}")
        print("------- Final contenido -------")

        # Enviar respuesta HTTP con código 200 (OK)
        self.send_response(200)
        # Enviamos la cabecera HTTP 'Content-type' para informar al cliente que el contenido de la respuesta
        # es HTML. Esto es importante porque el navegador u otro cliente necesita saber cómo interpretar 
        # los datos que recibe. Al especificar 'text/html', garantizamos que el cliente lo renderice como 
        # una página web. Sin esta cabecera, el cliente podría no saber cómo procesar correctamente la respuesta.
        self.send_header('Content-type', 'text/html')
        # Indicamos que no añadimos encabezados adicionales
        self.end_headers()

        # Enviamos el contenido del formulario al cliente, codificado en UTF-8
        self.wfile.write(bytes(html_calc_triangulo, 'utf-8'))
        # Escribimos el contenido HTML en el cuerpo de la respuesta. 
        # El método 'bytes' convierte la cadena de texto 'html_calc_triangulo' a formato binario usando 
        # la codificación UTF-8. Usamos UTF-8 porque es la codificación estándar para manejar caracteres
        # internacionales y especiales (como tildes o eñes) en HTML. Si no usamos UTF-8, podría haber errores
        # al mostrar caracteres no ASCII en la página, especialmente en español (como "á", "ñ").

    def do_POST(self):
        """
        Maneja las solicitudes POST procesando los datos enviados y devolviendo
        el cálculo del área.

        self: Representa la instancia actual del manejador que procesa
        esta solicitud POST. A través de self, accedemos a detalles como
        las cabeceras, los datos enviados y los métodos para enviar la respuesta.

        Este método se ejecuta cuando el servidor recibe una solicitud POST del cliente
        (como cuando un usuario envía un formulario desde un navegador). 

        Procesa los datos enviados por el cliente (base y altura del triángulo),
        calcula el área, y devuelve una página HTML mostrando el resultado del cálculo.
        """
        # Imprimimos detalles del objeto self y datos de la solicitud
        print("------- Contenido del request POST -------")
        print(f"path = {self.path}") # Ruta solicitada por el cliente
        for key, value in self.__dict__.items(): # Atributos de la instancia
            print (f"Atributo de instancia ='{key}' contiene {value}")
        
        # Obtenemos el tamaño del contenido enviado por el cliente en el cuerpo de la solicitud
        content_length = int(self.headers.get('Content-Length'))

        # Leemos los datos enviados por el cliente
        post_data = self.rfile.read(content_length)
        print(f"post data = {post_data}") # Muestra los datos en bruto

        # Parseamos los datos para convertirlos en un diccionario de parámetros
        params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        print(f"parametros ={params}") # Diccionario con los parámetros recibidos
        
        # Extraemos los valores de 'base' y 'altura' del diccionario y los convertimos a flotantes
        base = float(params['base'][0])
        altura = float(params['altura'][0])
        print("------- Contenido del request -------")

        # Enviamos una respuesta HTTP con el cálculo
        self.send_response(200)  # Código 200 significa que la solicitud fue exitosa
        self.send_header('Content-type', 'text/html') # Indicamos que el contenido devuelto es HTML
        self.end_headers()

        # Generamos el HTML con el resultado y lo enviamos al cliente
        self.wfile.write(bytes(genera_resultado(base, altura), 'utf-8')) # Codificación UTF-8
        


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, puerto=8000):
    """
    Configura y arranca el servidor HTTP en localhost.

    Args:
        server_class: Clase del servidor HTTP.
        handler_class: Clase que maneja las solicitudes HTTP.
        puerto (int): Puerto en el que se levantará el servidor.
    """
    server_address = ('', puerto)  # Dirección del servidor ('', puerto) significa localhost en el puerto especificado
    httpd = server_class(server_address, handler_class)  # Crear la instancia del servidor
    print(f"Servidor levantado en http://localhost:{puerto}")
    httpd.serve_forever()  # Iniciar el servidor para recibir solicitudes

# Arrancamos el servidor en el puerto 8027 con nuestro manejador definido
run(handler_class=LMCDPRequestHandler, puerto=8027)

