import argparse
import socket
import requests
import json


def push_ip(webhook_url):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]

    content = {
        "content": f"I'm alive!!! My IP is **{local_ip}**",
    }
    headers = {
        "Content-Type": "application/json",
    }
    requests.post(webhook_url, json=content, headers=headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--webhookUrl", type=str, help="Webhook URL")
    args = parser.parse_args()
    push_ip(args.webhookUrl)
