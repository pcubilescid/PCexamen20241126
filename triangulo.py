from http.server import HTTPServer , BaseHTTPRequestHandler
import urllib.parse

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
    
    def do_GET(self):
        print("------- Contenido del request SELF-------")
        print(f"path = {self.path}")
        for key, value in self.__dict__.items():
            print (f"Atributo de instancia ='{key}' contiene {value}")
        print("------- Final contenido -------")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(html_calc_triangulo, 'utf-8'))

    def do_POST(self):
        print("------- Contenido del request POST -------")
        print(f"path = {self.path}")
        for key, value in self.__dict__.items():
            print (f"Atributo de instancia ='{key}' contiene {value}")
        content_length = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_length)
        print(f"post data = {post_data}")
        params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        print(f"parametros ={params}")
                # Extract base and height
        base = float(params['base'][0])
        altura = float(params['altura'][0])
        print("------- Contenido del request -------")

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(genera_resultado(base, altura), 'utf-8'))
        #self.wfile.write(bytes(genera_resultado(base, altura), 'iso-8859-1'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, puerto=8000):
    server_address = ('', puerto)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor levantado en http://localhost:{puerto}")
    httpd.serve_forever()

run(handler_class = LMCDPRequestHandler, puerto=8027)

