import socket, sys
def t(name, raw):
    try:
        s = socket.socket(socket.AF_UNIX); s.settimeout(5)
        s.connect('/tmp/opencode/gh/t.sock')
        s.sendall(raw)
        resp = s.recv(300).decode(errors='replace').split('\r\n')[0]
        print(f"  {name:32} -> {resp}")
        s.close()
    except Exception as e:
        print(f"  {name:32} -> EXCEPCION {e}")
print("=== Pruebas de cabecera Host contra Gunicorn 27 ===")
t("Host normal", b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
t("Host duplicado", b"GET / HTTP/1.1\r\nHost: localhost\r\nHost: localhost\r\n\r\n")
t("Host vacio", b"GET / HTTP/1.1\r\nHost: \r\n\r\n")
t("Host con IP:port", b"GET / HTTP/1.1\r\nHost: 3.14.15.16:80\r\n\r\n")
t("Sin Host", b"GET / HTTP/1.1\r\n\r\n")
t("Host con puerto 80 explicito", b"GET / HTTP/1.1\r\nHost: localhost:80\r\n\r\n")
