import socket
import urllib.request
import json


def push_ip():
    with open("config.json", "r") as file:
        config = json.load(file)

    url = config["discord_webhook_url"]

    headers = {
        "Content-Type": "application/json",
    }

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]

    content = {
        "content": f"I'm alive!!! My IP is **{local_ip}**",
    }

    data = json.dumps(content).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(request) as response:
        response_data = response.read()
        print(response_data.decode("utf-8"))


def on_boot():
    push_ip()


if __name__ == "__main__":
    on_boot()
