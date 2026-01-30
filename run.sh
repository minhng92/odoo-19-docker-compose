#!/bin/bash
set -euo pipefail

# Parse named arguments (required: destination/port/chat; optional: password)
DESTINATION=""
PORT=""
CHAT=""
PASSWORD=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --destination)
      DESTINATION="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --chat)
      CHAT="$2"
      shift 2
      ;;
    --password)
      PASSWORD="$2"
      shift 2
      ;;
    *)
      echo "Error: Unknown option: $1" >&2
      echo "Usage: $0 --destination <path> --port <port> --chat <chat_port> [--password <master_password>]" >&2
      exit 1
      ;;
  esac
done

# Validate all required arguments are provided
if [[ -z "$DESTINATION" ]] || [[ -z "$PORT" ]] || [[ -z "$CHAT" ]]; then
  echo "Error: Missing required arguments" >&2
  echo "Usage: $0 --destination <path> --port <port> --chat <chat_port> [--password <master_password>]" >&2
  exit 1
fi

# Clone Odoo directory
git clone --depth=1 https://github.com/minhng92/odoo-19-docker-compose $DESTINATION
rm -rf $DESTINATION/.git

# Determine master password (use provided value or config default)
CONFIG_PATH="$DESTINATION/etc/odoo.conf"
DEFAULT_ADMIN_PASSWD="$(grep -E '^[[:space:]]*admin_passwd[[:space:]]*=' "$CONFIG_PATH" | head -n 1 | sed -E 's/^[[:space:]]*admin_passwd[[:space:]]*=[[:space:]]*//')"
MASTER_PASSWORD="${PASSWORD:-$DEFAULT_ADMIN_PASSWD}"

escape_sed_replacement() {
  printf '%s' "$1" | sed -e 's/[\\/&]/\\&/g'
}

# Create PostgreSQL directory
mkdir -p $DESTINATION/postgresql

# Change ownership to current user and set restrictive permissions for security
sudo chown -R $USER:$USER $DESTINATION
sudo chmod -R 700 $DESTINATION  # Only the user has access

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "Running on macOS. Skipping inotify configuration."
else
  # System configuration
  if grep -qF "fs.inotify.max_user_watches" /etc/sysctl.conf; then
    echo $(grep -F "fs.inotify.max_user_watches" /etc/sysctl.conf)
  else
    echo "fs.inotify.max_user_watches = 524288" | sudo tee -a /etc/sysctl.conf
  fi
  sudo sysctl -p
fi

# Set ports in docker-compose.yml and optionally update master password
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS sed syntax
  sed -i '' 's/10019/'$PORT'/g' $DESTINATION/docker-compose.yml
  sed -i '' 's/20019/'$CHAT'/g' $DESTINATION/docker-compose.yml
  if [[ -n "$PASSWORD" ]]; then
    ESCAPED_PASSWORD="$(escape_sed_replacement "$MASTER_PASSWORD")"
    sed -i '' -E "s/^[[:space:]]*admin_passwd[[:space:]]*=.*/admin_passwd = $ESCAPED_PASSWORD/" "$CONFIG_PATH"
  fi
else
  # Linux sed syntax
  sed -i 's/10019/'$PORT'/g' $DESTINATION/docker-compose.yml
  sed -i 's/20019/'$CHAT'/g' $DESTINATION/docker-compose.yml
  if [[ -n "$PASSWORD" ]]; then
    ESCAPED_PASSWORD="$(escape_sed_replacement "$MASTER_PASSWORD")"
    sed -i -E "s/^[[:space:]]*admin_passwd[[:space:]]*=.*/admin_passwd = $ESCAPED_PASSWORD/" "$CONFIG_PATH"
  fi
fi

# Set file and directory permissions after installation
find $DESTINATION -type f -exec chmod 644 {} \;
find $DESTINATION -type d -exec chmod 755 {} \;

chmod +x $DESTINATION/entrypoint.sh

# Check if docker needs sudo - docker ps exits with error if user lacks permissions
DOCKER_SUDO=""
if ! docker ps >/dev/null 2>&1; then
  echo "Docker requires sudo privileges"
  DOCKER_SUDO="sudo"
fi

# Run Odoo
if ! is_present="$(type -p "docker-compose")" || [[ -z $is_present ]]; then
  $DOCKER_SUDO docker compose -f $DESTINATION/docker-compose.yml up -d
else
  $DOCKER_SUDO docker-compose -f $DESTINATION/docker-compose.yml up -d
fi


echo "Odoo started at http://localhost:$PORT | Master Password: $MASTER_PASSWORD | Live chat port: $CHAT"
