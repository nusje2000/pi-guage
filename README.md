# Requirements

## Display Client
Display support

## Data Collection Client
- nodejs
- npm

## Registering services
Create a `data_collector.service` or `data_display.service` depending on what you are registering inside `/etc/systemd/system`.

### Data collector
```
[Unit]
Description=Data Collection Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/pi/code 
ExecStart=/usr/bin/npm run serve

[Install]
WantedBy=multi-user.target
```

### Display
```
[Unit]
Description=Data Display
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/pi/code
ExecStart=/usr/bin/python3 main.py

[Install]
WantedBy=multi-user.target
```

### Enabling the service
```bash
systemctl daemon-reload
systemctl enable {service_name}.service
systemctl start {service_name}.service
```
