#!/usr/bin/env python3

import socket
import datetime
import threading
import json


# Configuration #

host = "0.0.0.0"
port = 2222
log_file = "honeypot.log"
sensor_name = "ssh-honeypot-01"
network_zone = "internal" # or "external" depending on placement


# Logging Helper #

def log_event(event):
# Writes a single JSON event to the log file.
# Each line is one complete event.

    event["timestamp"] = datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y %H:%M:%S")
    event["sensor"] = sensor_name
    event["network_zone"] = network_zone

    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")


# Client Handler #

def handle_client(client_socket, client_address):
# Handles one incoming TCP connection.

    source_ip, source_port = client_address

    # Log the connection event
    log_event({
        "event_type": "connection",
        "protocol": "tcp",
        "source_ip": source_ip,
        "source_port": source_port,
        "destination_port": port
    })

    try:
        # send a fake SSH banner
        fake_banner = b"SSH-2.0-OpenSSH_7.4\r\n"
        client_socket.sendall(fake_banner)

        # receive up to 1024 bytes
        data = client_socket.recv(1024)

        if data:
            payload = data.decode(errors="replace").strip()

            # log received payload
            log_event({
                "event_type": "payload",
                "protocol": "tcp",
                "source_ip": source_ip,
                "source_port": source_port,
                "payload": payload
            })

    except Exception as e:
        # log errors as their own event type
        log_event({
            "event_type": "error",
            "source_ip": source_ip,
            "error": str(e)
        })

    finally:
        client_socket.close()

        # log connection close
        log_event({
            "event_type": "disconnect",
            "protocol": "tcp",
            "source_ip": source_ip,
            "source_port": source_port
        })


# Main Server Loop #

def start_honeypot():
# Starts the honeypot listener.

    log_event({
        "event_type": "startup",
        "message": "Honeypot started"
    })

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Honeypot listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )
        client_thread.start()


# Entry Point #

if __name__ == "__main__":
    start_honeypot()