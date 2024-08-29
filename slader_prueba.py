import socketpool
import wifi

# Conectar a la red Wi-Fi
wifi.radio.connect("Oh_rigth", "culoacido")
pool = socketpool.SocketPool(wifi.radio)

print("wifi.radio:", wifi.radio.hostname, wifi.radio.ipv4_address)
s = pool.socket()
s.bind(('', 80))
s.listen(5)

# Página HTML con un slider
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Control de Slider</title>
</head>
<body>
    <h1>Control de Servo</h1>
    <label for="slider">Ángulo del Servo:</label>
    <input type="range" id="slider" min="0" max="180" value="90" oninput="updateValue(this.value)">
    <p>Ángulo seleccionado: <span id="angleValue">90</span> grados</p>

    <script>
        function updateValue(value) {
            document.getElementById("angleValue").innerText = value;
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_angle?value=" + value, true);
            xhr.send();
        }
    </script>
</body>
</html>
"""

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    
    # Recibir datos del cliente
    buffer = bytearray(1024)  # Crear un buffer mutable
    bytes_received, address = conn.recvfrom_into(buffer)  # Recibir datos en el buffer
    request = buffer[:bytes_received].decode('utf-8')
    print("Received request:", request)

    # Analizar la solicitud del cliente
    if "GET / " in request:
        # Si la solicitud es para la página principal
        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html
        conn.send(response.encode('utf-8'))
    elif "GET /set_angle?value=" in request:
        # Si la solicitud es para ajustar el ángulo del slider
        angle = int(request.split("value=")[-1].split(" ")[0])
        print(f"Ángulo recibido: {angle} grados")
        # Aquí puedes agregar código para controlar el servo basado en el ángulo recibido
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nÁngulo recibido"
        conn.send(response.encode('utf-8'))

    conn.close()

