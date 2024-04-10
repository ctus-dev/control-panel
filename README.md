# CTUS Smartrack

## Install

```
cd ~
git clone https://github.com/ctus-dev/smartrack-pi.git
cd smartrack-pi
chmod +x install/install.sh
install/install.sh
```

### Update

-   After 04-10-2024

```
cd ~/smartrack-pi
smartrack update
```

-   Pre update

```
smartrack display message "Updating..."
sudo systemctl stop stats.service
sudo systemctl stop button.service
cd ~
sudo rm -d -r smartrack-pi
git clone https://github.com/ctus-dev/smartrack-pi.git
cd smartrack-pi
chmod +x install/update.sh
install/update.sh
```

### Post install or update

```
sudo reboot
```

## Operation

### CLI

-   Network Mode

```
smartrack dhcp

smartrack static 192.168.1.100 192.168.1.1
```

-   Display Stats

```
smartrack display stats

smartrack display stats false
```

-   Display Message

```
smartrack display message "A Test Message"
```

-   Display Message Multi Line ('+' between lines)

```
smartrack display message "A Test Message+Line 2"
```
