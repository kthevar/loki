#!/bin/bash

# Replace these paths and configuration options as needed
#LOKI_EXECUTABLE="./loki-linux-amd64"
LOKI_INSTALL_DIR="/opt/loki"
LOKI_CONFIG="loki-local-config.yaml"
LOKI_DATA_DIR="$LOKI_INSTALL_DIR/data" # Adjust as needed
LOKI_EXECUTABLE="loki-linux-amd64"
LOKI_USER="loki"
LOKI_GROUP="loki"
# Download and install Loki
cd $LOKI_INSTALL_DIR
curl -O -L "https://github.com/grafana/loki/releases/download/v2.8.4/loki-linux-amd64.zip"
unzip "loki-linux-amd64.zip"
chmod a+x "loki-linux-amd64"

# Download Loki and Promtail configuration files
wget https://raw.githubusercontent.com/grafana/loki/main/cmd/loki/loki-local-config.yaml
wget https://raw.githubusercontent.com/grafana/loki/main/clients/cmd/promtail/promtail-local-config.yaml

# Create the Loki systemd service file
sudo tee /etc/systemd/system/loki.service > /dev/null << EOF
[Unit]
Description=Grafana Loki Service
After=network.target

[Service]
User=$LOKI_USER
Group=$LOKI_GROUP
Type=simple
ExecStart=$LOKI_INSTALL_DIR/$LOKI_EXECUTABLE -config.file=$LOKI_INSTALL_DIR/$LOKI_CONFIG
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create the Loki user and group
sudo groupadd $LOKI_GROUP
sudo useradd -r -M -s /bin/false -g $LOKI_GROUP $LOKI_USER

# Set permissions
sudo mkdir -p $LOKI_DATA_DIR
sudo chown -R $LOKI_USER:$LOKI_GROUP $LOKI_DATA_DIR

# Enable and start the Loki service
sudo systemctl enable loki
sudo systemctl start loki

# Display service status
sudo systemctl status loki