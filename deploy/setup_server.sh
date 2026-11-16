#!/usr/bin/env bash
# One-click deployment script for Alibaba Cloud Linux / Ubuntu / Debian servers.
# Configures a Python venv, Gunicorn (1 worker, 4 threads for SQLite safety),
# a systemd background service, and Nginx reverse proxy on port 80.

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming.git}"
APP_DIR="${APP_DIR:-/opt/address-book}"
SERVICE_NAME="address-book"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Please run this script as root (e.g., sudo bash deploy/setup_server.sh)."
  exit 1
fi

echo "==> [1/5] Installing system packages (git, python3, nginx)..."
if command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y git python3 python3-venv python3-pip nginx curl
elif command -v dnf >/dev/null 2>&1; then
  dnf install -y git python3 python3-pip nginx curl
elif command -v yum >/dev/null 2>&1; then
  yum install -y git python3 python3-pip nginx curl
else
  echo "Unsupported package manager. Install git, python3, venv, pip, and nginx manually."
  exit 1
fi

echo "==> [2/5] Syncing repository into ${APP_DIR}..."
if [[ -d "${APP_DIR}/.git" ]]; then
  git -C "${APP_DIR}" fetch origin
  git -C "${APP_DIR}" reset --hard origin/main
else
  rm -rf "${APP_DIR}"
  git clone --depth 1 "${REPO_URL}" "${APP_DIR}"
fi

echo "==> [3/5] Setting up Python virtual environment and dependencies..."
python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/pip" install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ || "${APP_DIR}/.venv/bin/pip" install --upgrade pip
"${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt" gunicorn -i https://mirrors.aliyun.com/pypi/simple/ \
  || "${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt" gunicorn

mkdir -p "${APP_DIR}/instance"

echo "==> [4/5] Configuring systemd service (${SERVICE_NAME})..."
cat >/etc/systemd/system/${SERVICE_NAME}.service <<EOF
[Unit]
Description=Address Book Flask Application (Gunicorn)
After=network.target

[Service]
Type=simple
WorkingDirectory=${APP_DIR}
Environment="ADDRESS_BOOK_DB=${APP_DIR}/instance/address_book.db"
ExecStart=${APP_DIR}/.venv/bin/gunicorn -w 1 --threads 4 -b 127.0.0.1:5000 --access-logfile - --error-logfile - app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo "==> [5/5] Configuring Nginx reverse proxy on port 80..."
NGINX_CONF_CONTENT=$(cat <<'EOF'
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 12M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
)

if [[ -d /etc/nginx/sites-available && -d /etc/nginx/sites-enabled ]]; then
  printf "%s\n" "${NGINX_CONF_CONTENT}" > /etc/nginx/sites-available/${SERVICE_NAME}
  rm -f /etc/nginx/sites-enabled/default
  ln -sf /etc/nginx/sites-available/${SERVICE_NAME} /etc/nginx/sites-enabled/${SERVICE_NAME}
else
  # RHEL / Alibaba Cloud Linux style (/etc/nginx/conf.d)
  if [[ -f /etc/nginx/nginx.conf ]]; then
    sed -i 's/listen       80 default_server;/listen       80;/g' /etc/nginx/nginx.conf || true
    sed -i 's/listen       \[::\]:80 default_server;/# listen [::]:80 default_server;/g' /etc/nginx/nginx.conf || true
  fi
  printf "%s\n" "${NGINX_CONF_CONTENT}" > /etc/nginx/conf.d/${SERVICE_NAME}.conf
fi

nginx -t
systemctl enable nginx
systemctl restart nginx

sleep 2
echo "==> Verifying local health endpoint..."
curl -fsS http://127.0.0.1/api/health
echo ""
echo "Deployment succeeded! Visit http://$(curl -fsS --max-time 3 ifconfig.me 2>/dev/null || echo '<YOUR_PUBLIC_IP>')"
