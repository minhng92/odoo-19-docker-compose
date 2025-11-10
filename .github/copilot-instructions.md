# Copilot Instructions for Odoo 19 Docker Compose

## Project Overview

This is a Docker Compose setup for running **Odoo 19.0** with PostgreSQL 18. It supports multiple Odoo instances on a single server with configurable ports.

### Architecture
- **Services**: Two containers (`db` for PostgreSQL 18, `odoo19` for Odoo 19)
- **Volume mounts**: `./addons` → `/mnt/extra-addons`, `./etc` → `/etc/odoo`, `./postgresql` → `/var/lib/postgresql/18/docker`
- **Port mapping**: Default 10019 (Odoo), 20019 (live chat/longpolling)
- **Custom entrypoint**: `entrypoint.sh` handles DB connection, pip installs, and logrotate setup

## Key Files & Their Purpose

- **`docker-compose.yml`**: Service definitions. Both services run as `root` user. Note PostgreSQL 18's version-specific PGDATA path.
- **`entrypoint.sh`**: Installs Python packages from `etc/requirements.txt`, configures logrotate, waits for PostgreSQL, then starts Odoo with dynamic DB credentials.
- **`run.sh`**: One-command deployment script. Takes 3 args: folder name, Odoo port, chat port. Clones repo, sets permissions, configures ports via sed, starts containers.
- **`etc/odoo.conf`**: Odoo configuration. Key settings: `addons_path = /mnt/extra-addons`, `admin_passwd = minhng.info` (L75), `dev_mode = reload`, logs to `/etc/odoo/odoo-server.log`.
- **`etc/requirements.txt`**: Python dependencies installed at container startup via pip.
- **`etc/logrotate`**: Rotates `/etc/odoo/*.log` files daily, keeps 3 days.

## Critical Workflows

### Starting/Stopping Odoo
```bash
docker-compose up -d              # Start detached
docker-compose restart            # Restart services
docker-compose down               # Stop and remove containers
```

### Adding Custom Modules
Place custom addons in `addons/` directory. They're automatically mounted to `/mnt/extra-addons` (configured in `odoo.conf`). Restart containers after adding modules.

### Multi-Instance Deployment
Use `run.sh` with 3 parameters:
```bash
./run.sh <folder-name> <odoo-port> <chat-port>
# Example: ./run.sh odoo-prod 10019 20019
```
This clones the repo, sets ports in `docker-compose.yml`, and starts containers.

### Permission Issues
If containers can't access directories:
```bash
sudo chmod -R 777 addons etc postgresql
```
The `run.sh` script sets `chmod 700` initially, then `644` for files and `755` for directories.

### Installing Python Packages
1. Add package to `etc/requirements.txt` (e.g., `paramiko==2.7.2`)
2. Restart containers (entrypoint.sh automatically installs at startup)
3. Alternatively, exec into container: `docker-compose exec odoo19 pip3 install <package>`

### Production Configuration
- **Change default password**: Edit `admin_passwd` in `etc/odoo.conf` (L75)
- **Nginx for live chat**: Proxy `/longpolling/` to port 20019 (see README L95-101)
- **Worker mode**: Set `workers` in `etc/odoo.conf` for production (default is single-threaded)
- **Restart policy**: Already set to `restart: always` in `docker-compose.yml`

## Project-Specific Conventions

### Environment Variables (docker-compose.yml)
- `PIP_BREAK_SYSTEM_PACKAGES=1`: Required for pip to work in Debian 12+ containers
- PostgreSQL credentials: `POSTGRES_USER=odoo`, `POSTGRES_PASSWORD=odoo19@2025`
- Odoo connects via: `HOST=db`, `USER=odoo`, `PASSWORD=odoo19@2025`

### Entrypoint Behavior
- `entrypoint.sh` dynamically reads DB config from env vars OR `odoo.conf`
- Installs logrotate and starts cron daemon for log rotation
- Waits for PostgreSQL (`wait-for-psql.py`) before starting Odoo
- All DB args are passed explicitly to Odoo process

### Port Customization
Modify ports in `docker-compose.yml`:
```yaml
ports:
  - "10019:8069"  # Change 10019 to desired port
  - "20019:8072"  # Change 20019 to desired chat port
```

### File System Limits (Linux)
For multiple instances, increase inotify watches:
```bash
echo "fs.inotify.max_user_watches = 524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
The `run.sh` script does this automatically (skips on macOS).

## Common Debugging

- **Logs**: Check `etc/odoo-server.log` for Odoo logs
- **DB connection issues**: Verify PostgreSQL is running: `docker-compose ps`
- **Module not loading**: Ensure addons are in `addons/` and permissions are correct (777 or 755)
- **Port conflicts**: Check if ports 10019/20019 are already in use: `netstat -tuln | grep 10019`

## DO NOT

- **Never commit** `postgresql/` directory (contains database data)
- **Never hardcode** new passwords without updating both `docker-compose.yml` and `etc/odoo.conf`
- **Never run** `docker-compose up` without `-d` for servers (blocks terminal)
- **Never modify** `entrypoint.sh` without making it executable: `chmod +x entrypoint.sh`
