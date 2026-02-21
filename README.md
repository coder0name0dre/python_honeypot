# Python SSH Honeypot

This is a low interaction Python TCP honeypot.

It pretends to be an SSH service, safely logs connection attempts, and writes structured JSON logs that are easy to ingest into a SIEM.

This script:

- Listens on a TCP port (default `2222`)
- Accepts incoming connections
- Sends a fake SSH banner
- Logs what connects and what data is sent
- Never executes commands
- Never exposes you system
- Only observes and records

---

## Requirements

- Python 3.8+
- Linux or macOS recommended (Windows works for testing)
- No external Python libraries required

---

## How To Run

1. Clone the repository:

```
git clone https://github.com/coder0name0dre/python_honeypot.git
cd python-honeypot
```

2. Run the script:

```
python3 honeypot.py
```

3. You should see:

`Honeypot listening on 0.0.0.0:2222`

The honeypot is now running.

---

## How To Test It Safely (locally)

From another terminal on the same machine:

```
nc localhost 2222
```

You should receive a fake SSH banner:

`SSH-2.0-OpenSSH_7.4`

Check the log file:

```
cat honeypot.log
```

---

## Log Format (SIEM friendly)

Each line in `honeypot.log` is one JSON event:

```
{
"event_type": "connection",
"protocol": "tcp",
"source_ip": "10.12.4.23",
"source_port": 49822,
"destination_port": 2222,
"timestamp": "08-02-2026 18:41:15",
"sensor": "ssh-honeypot-01",
"network_zone": "internal"
}
```

Why this matters:

- Easy SIEM ingestion
- No regex parsing
- Simple correlation and alerting

---

## Running Safely On A Linux Server

1. Create a non privileged user

```
sudo adduser honeypot
sudo su - honeypot
```

2. Allow only the poneypot port

```
sudo ufw allow 2222/tcp
sudo ufw enable
```

3. Run using tmux (simple and safe)

```
tmux new -s honeypot
python3 honeypot.py
```

Detach with:

```
Ctrl + B, then D
```

---

## Stopping The Honeypot

If running interactively:

```
Ctrl + C
```

If running in tmux:

```
tmux attach -t honeypot
Ctrl + C
```

---

## Notice

- Only log traffic sent to you
- Do not attempt to identify or retaliate againsty sources
- Do not imitate real production services on networks you don't own
- Follow local laws and cloud provider terms

This honeypot is passive and defensive.

---

## License

This project is licensed under the [MIT License](https://github.com/coder0name0dre/python_honeypot/blob/main/LICENSE).