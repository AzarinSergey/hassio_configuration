# Installation
### Preparing the Raspberry 3 model B V1.2 device

* Download [Raspberry OS][1] (light version recommended)
* You can use [Balena][2] to write OS image to SD card
* SSH can be enabled by placing a file named ssh, without any extension, onto the boot partition of the SD card from another computer. 



### Configure Raspberry OS
##### Configure SSH
1. Use SSH to connect with default credentials:
login - 'pi', password  - 'raspberry'.
\
Don't forget to change password for 'pi' user by ```$ rasp-config```

2. Add user:
```sh
$ sudo adduser yourusername
```

3. Add user to group 'sudo':
```sh 
$ sudo usermod -aG sudo yourusername
```

4. Relogin SSH client with new user.

##### Update hardware and packages

1. Hardware
```sh
$ sudo rpi-update
```

2. Reboot Raspberry
```sh
$ sudo reboot
```

3. Update packages list
```sh
$ sudo apt-get update
```

4. Update packages: 
```sh
$ sudo apt-get -y upgrade
```

##### Configure networking

1. Open file ```sudo nano /etc/network/interfaces``` and past text:
```
auto lo
iface lo inet loopback

#iface eth0 inet manual

allow-hotplug eth0
iface eth0 inet static
    address 192.168.0.100
    netmask 255.255.255.0
    gateway 192.168.0.1
```

2. Set IP address and gateway as necessary. (gateway - usually it's IP address of router)
3. Press 'Ctrl-X' to exit and 'Y' to save changes.
4. Reboot device ```sudo reboot```.

##### Configure locale
Go to ```sudo raspi-config``` and select:

 - 8 Update
 - 4 Localisation Options / I1 Change Locale (RU UTF-8)
 - 4 Localisation Options / I2 Change Timezone

### Install Hass.io and requirements
##### Install packages:
```sh
sudo apt-get install -y \
bash curl git jq avahi-daemon dbus apparmor-utils network-manager \
libavahi-compat-libdnssd-dev libatlas3-base apt-transport-https \
ca-certificates socat software-properties-common ftpd mc 
```
And ```sudo reboot``` device.

##### Install Docker:
 1. Run command:
```sh 
sudo curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
```
2. Add group 'docker' ```sudo groupadd docker``` and add user to new group ```sudo gpasswd -a myusername docker```, ```newgrp docker```.

##### Install Portainer
```sh
docker pull portainer/portainer
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

##### Install Hass.io

1. Go to root ```sudo su```.

2. Install hass.io ([manual][5]) : 
```sh
$ curl -sL https://raw.githubusercontent.com/home-assistant/supervised-installer/master/installer.sh 
\ | bash -s -- -m raspberrypi3
```

Now Hass.io UI on - IP adress:8123
\

[1]: <https://www.raspberrypi.org/>
[2]: <https://www.balena.io/etcher/>
[3]: <https://materialdesignicons.com/>
[4]: <https://www.home-assistant.io/lovelace/>
[5]: <https://github.com/home-assistant/supervised-installer>
