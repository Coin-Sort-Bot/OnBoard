import socket
import requests
import json


def push_ip():
    with open("config.json", "r") as file:
        config = json.load(file)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]

    content = {
        "content": f"I'm alive!!! My IP is **{local_ip}**",
    }
    url = config["discord_webhook_url"]
    headers = {
        "Content-Type": "application/json",
    }
    requests.push(url, json=content, headers=headers)


def on_boot():
    push_ip()


if __name__ == "__main__":
    on_boot()
