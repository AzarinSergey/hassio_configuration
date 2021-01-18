# Developer notes
\
Configuration repository location on Raspberry:
```sh
$ cd /usr/share/hassio/homeassistant
```
\
Other useful commands:
```sh
$ ifconfig
$ rasp-config
$ docker cp
$ nano /etc/network/interfaces
$ wget URL
$ cat FILENAME
$ su myusername
$ groups
$ sudo iptables -t filter -A INPUT -p tcp --dport 8123 -j ACCEPT
$ sudo iptables -t filter -A OUTPUT -p tcp --dport 8123 -j ACCEPT
$ ip route show (| grep default)
$ netstat -a |grep 8123
$ getconf LONG_BIT
```
\

Dev env
```sh
hass --config /workspaces/hassio-fork/config

Use material design [icons][3] to improve your [lovelace UI][4]

[1]: <https://www.raspberrypi.org/>
[2]: <https://www.balena.io/etcher/>
[3]: <https://materialdesignicons.com/>
[4]: <https://www.home-assistant.io/lovelace/>
[5]: <https://github.com/home-assistant/supervised-installer>