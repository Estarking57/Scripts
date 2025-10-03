# Basics_Commands
Update packages (Basic) 
```sh
sudo apt update && sudo apt upgrade -y 
```
Update packages and flatpaks and do clean up
```sh
 sudo apt update && sudo apt upgrade -y && flatpak update -y && sudo apt autoremove -y && sudo apt clean
```
