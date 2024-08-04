#!/usr/bin/env python3

import json
import requests
from argparse import ArgumentParser


def _add_slash_suffix(url: str) -> str:
    if url[-1] != "/":
        return url + "/"
    return url


def get_token(base_url: str, token_path: str, username: str, password: str) -> str:
    # Make sure addresses end with '/'.
    base_url = _add_slash_suffix(base_url)
    token_path = _add_slash_suffix(token_path)

    # Make a request.
    url = f"{base_url}{token_path}"
    data = json.dumps({"username": username, "password": password})
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, data=data, headers=headers)

    # Throw an exception if status is not '200'.
    response.raise_for_status()

    # Response is returned as formatted JSON text.
    return json.dumps(json.loads(response.text), indent=4)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Get authentication token for provided credentials."
    )
    parser.add_argument(
        "--base_url",
        default="http://localhost:8000/",
        help="Base URL. Default: %(default)s",
    )
    parser.add_argument(
        "--token_path",
        default="api/token-auth/",
        help="Token path. Default: %(default)s",
    )
    parser.add_argument("-u", "--username", required=True, help="User name.")
    parser.add_argument("-p", "--password", required=True, help="Password.")
    args = parser.parse_args()

    token_json = get_token(args.base_url, args.token_path, args.username, args.password)
    print(token_json)
