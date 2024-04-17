#!/bin/bash


function set_alias() {
  local alias=$1
  local alias_target=$2

  if sudo grep -q "alias $alias=" ~/.bashrc; then
    sed -i "s@alias $alias='.*'@alias $alias=$alias_target@" ~/.bashrc
  else
    echo "alias $alias=$alias_target" >> ~/.bashrc
  fi
}

# smartrack module
# shellcheck source=/dev/null
source .venv/bin/activate
pip install --upgrade -r requirements.txt
chmod 0777 smartrack_pi/config.json # allows webpage to write to config

# webserver
sudo cp install/nginx/smartrack-settings /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/smartrack-settings /etc/nginx/sites-enabled
sudo systemctl restart nginx


# set alias for smartrack cli
alias="smartrack"
alias_target="'/home/smartrack/smartrack-pi/.venv/bin/python /home/smartrack/smartrack-pi/smartrack_pi/cli.py'"
set_alias "$alias" "$alias_target"

# services
sudo cp install/services/stats.service /etc/systemd/system/stats.service
sudo cp install/services/button.service /etc/systemd/system/button.service
sudo cp install/services/smartrack-settings.service /etc/systemd/system/smartrack-settings.service
sudo systemctl daemon-reload
sudo systemctl enable stats.service
sudo systemctl enable button.service
sudo systemctl enable smartrack-settings.service
sudo systemctl start stats.service
sudo systemctl start button.service
sudo systemctl start smartrack-settings.service