import socketpool
import wifi
import pwmio
import board

# Conectar a la red Wi-Fi
wifi.radio.connect("Oh_rigth", "culoacido")
pool = socketpool.SocketPool(wifi.radio)

print("wifi.radio:", wifi.radio.hostname, wifi.radio.ipv4_address)
s = pool.socket()
s.bind(('', 80))
s.listen(5)

# Configuración del servomotor
servo = pwmio.PWMOut(board.GP0, frequency=50)  # Usando GP0 como pin de ejemplo
min_duty = 1638  # 2.5% de duty cycle
max_duty = 8192  # 12.5% de duty cycle

# Función para mapear el ángulo a un valor de duty cycle
def map_angle_to_duty(angle):
    return min_duty + (max_duty - min_duty) * angle // 180

# Inicializar el servomotor en 0 grados
servo.duty_cycle = map_angle_to_duty(0)
print("Servo inicializado a 0 grados")

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
        
        # Ajustar el servomotor basado en el ángulo recibido
        duty_cycle = map_angle_to_duty(angle)
        servo.duty_cycle = duty_cycle
        print(f"Duty cycle ajustado: {duty_cycle}")
        
        response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nÁngulo recibido"
        conn.send(response.encode('utf-8'))

    conn.close()

