docker build

docker build -t pyqt .


docker run 

docker run -e DISPLAY=$(ipconfig | grep -A 1 'Wireless LAN adapter Wi-Fi' | grep 'IPv4 Address' | awk '{print $14}'):0 -v /tmp/.X11-unix:/tmp/.X11-unix pyqt


this right now works only on linux distro
