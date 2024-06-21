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

BASE_URL="http://localhost:8000/"
TOKEN_PATH="api/token-auth/"
DEFAULT_USERNAME="opiekun1"
DEFAULT_PASSWORD="opiekun1"
USERNAME=${1:-$DEFAULT_USERNAME}
PASSWORD=${2:-$DEFAULT_PASSWORD}

TOKEN=$(curl -s -X "POST" \
  "${BASE_URL}${TOKEN_PATH}" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
  \"username\": \"$USERNAME\",
  \"password\": \"$PASSWORD\"
}" | jq -r .token)

if [ -n "$TOKEN" ]; then
  copy_to_clipboard "$TOKEN"
else
  echo "Failed to retrieve token."
fi
