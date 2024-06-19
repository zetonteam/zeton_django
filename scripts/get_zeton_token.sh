#!/usr/bin/env bash

command_exists() {
  command -v "$1" &> /dev/null
}

if ! command_exists curl; then
  echo "'curl' is not installed. Please install 'curl' to use this script."
  exit 1
fi

if ! command_exists jq; then
  echo "'jq' is not installed. Please install 'jq' to use this script."
  exit 1
fi

copy_to_clipboard() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command_exists xclip; then
      echo "$1" | xclip -selection clipboard
      echo "Token has been copied to clipboard using xclip!"
    else
      echo "'xclip' not found. Token: $1"
    fi
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "$1" | pbcopy
    echo "Token has been copied to clipboard using pbcopy!"
  else
    echo "Unsupported OS. This script works on GNU/Linux and MacOS only."
  fi
}

TOKEN=$(curl -s -X 'POST' \
  'http://localhost:8000/api/token-auth/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "opiekun1",
  "password": "opiekun1"
}' | jq -r .token)

if [ -n "$TOKEN" ]; then
  copy_to_clipboard "$TOKEN"
else
  echo "Failed to retrieve token."
fi
