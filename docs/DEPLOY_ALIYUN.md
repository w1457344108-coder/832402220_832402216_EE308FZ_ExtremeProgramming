# Alibaba Cloud (ECS / Lightweight App Server) Deployment Guide

This guide deploys the Address Book web app using **Gunicorn + systemd + Nginx** on port `80` with persistent SQLite storage at `/opt/address-book/instance/address_book.db`.

## Prerequisites

1. A Linux cloud server (Ubuntu 22.04/24.04, Debian 12, or Alibaba Cloud Linux 3).
2. Security group / firewall rules allowing inbound TCP port `80` (HTTP) and `22` (SSH).

## One-Step Setup (Run as `root` on the server)

```bash
git clone https://github.com/w1457344108-coder/832402220_832402216_EE308FZ_ExtremeProgramming.git /opt/address-book && bash /opt/address-book/deploy/setup_server.sh
```

If `git clone` from GitHub is slow in your region, you can alternatively upload the local repository via `scp` from your laptop:

```bash
# Run on your local machine
tar --exclude='.git' --exclude='.venv' --exclude='instance' -czf address-book.tar.gz -C /Users/zhaoyan/Documents/CodexAPIWorkspace/832402220_832402216_EE308FZ_ExtremeProgramming .
scp address-book.tar.gz root@<YOUR_PUBLIC_IP>:/tmp/
```

## Updating After Future Commits / PR Merges

```bash
bash /opt/address-book/deploy/setup_server.sh
```

## Useful Operations

```bash
systemctl status address-book
journalctl -u address-book -n 50 --no-pager
curl http://127.0.0.1/api/health
```
