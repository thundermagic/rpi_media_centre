# Media Centre on Raspberry Pi
This is a bundle of different docker containers to run a media centre. This would let you playback and manage media. 

**DISCLAIMER: NOT ALL THE SERVICES ARE CREATED BY ME. I HAVE JUST PUT THEM TOGETHER.**

Since this uses docker containers, it can be run on `amd64` platforms as well (i.e your windows or linux machine). 
This guide is generic, any platform specific changes would be highlighted with comments. This guide uses commands for `debian` and 
debian based systems (like `raspbian`). If you are using a different distro, please use the relevant commands. 

## Isn't Raspberry Pi under powered to run a media centre?
Raspberry Pi 4 actually makes a good low powered platform to run a home media centre system. It can't really handle video 
transcoding (can do couple of 720p transcoding and 1080p in some cases) but if you are using this for home purpose and 
all the video clients are under your control, you can choose the clients that would play most of the video content 
without transcoding (i.e direct play/stream).

I have been using a single Raspberry Pi 4 4GB version as a media centre since the day it was launched (actually couple of days after 
the release for delivery time). Before that I was using a Raspberry Pi 3B+ and that worked alright as well.  

RPi can direct play few video streams simultaneously without any issue, assuming your home network is good enough. Wired 
connectivity between clients and the media server would help.  

My home setup is all on one RPi 4 (overclocked to 2 GHz). For storage I have two HDD connected to the Pi and they are in RAID 1. I am using linux
software raid (mdadm). I am also running monitoring stuff on the same Pi (prometheus, grafana etc etc). There has been no performance
issues with the Raspberry Pi. I have amazon firestick 4K as video clients connected to TVs. This can play most of the video content. 
And if there is any content that requires transcoding to play, then I just get the format that would direct play on firestick. 
If I am managing video content then I can control which video formats I get. This is quite easy to do using services like 
radarr/sonarr/lidarr. You can exclude video/audio formats that you don't want.

You would need active cooling for RPi 4. It gets HOT! I use [40mm heatsink](https://www.amazon.co.uk/Easycargo-conductive-TEC1-12706-Thermoelectric-40mmx40mmx11mm/dp/B07D4FVC61/ref=sr_1_1?crid=30Z05ERNBH3F7&keywords=40mm+heatsink&qid=1568560208&s=gateway&sprefix=40mm+heat%2Caps%2C259&sr=8-1) 
with [noctua 5v fan](https://www.amazon.co.uk/Noctua-NF-A4x20-FLX-Premium-40x20mm/dp/B071J8CZP9/ref=sr_1_3_sspa?keywords=noctua+5v&qid=1568560244&s=gateway&sr=8-3-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFLUUNSTkU0Vk1DRUYmZW5jcnlwdGVkSWQ9QTEwMTc3MDUxVUtEOVMwQ0FFQlFFJmVuY3J5cHRlZEFkSWQ9QTA2OTY4MjExVEs2N1lVSE00Q0hXJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==)
 and this keeps RPi quite cool even under full load.

Yes, if you want to transcode video and want to serve content over the WAN to friends and family, then you would need something
more powerful. You can still use this guide, it would work regardless if you are using a RPi or something else.

## Services used
- Plex*: Main media server
- Transmission: Torrent client
- Openvpn: VPN client
- Radarr: Automated movie management and integration with torrent client
- Sonarr: Same as radarr but for TV shows
- Lidarr: Same as radarr but for Music
- Tautulli: Plex media server monitoring service
- Jackett: Torrent indexers proxy
- sonarr_netimport: A python script to fetch TV shows from tvdb.com and add them to sonarr
- radarr_netimport: Similar to sonarr_netimport but for radarr

Note: transmission and openvpn are in one container.  
*You can change this with other media server like Emby. See `docker-compose.yaml` file for details.  

If you don't want to use a specific service or use something different in its place, you can delete/change that service
in the `docker-compose.yaml` file. Most of the services that you would need for media centre have docker containers 
built by [linuxserver.io](https://www.linuxserver.io/)

## Prerequisite 
- docker
- docker-compose

Follow this guide if you have to install docker and docker-compose: https://github.com/thundermagic/rpi_media_centre/blob/master/docs/docker_install.md

## Quick start
Ok, lets run the media centre

**NOTE:** You can change where data is stored and use your own directory structure by editing `docker-compose.yaml`. More details are in the yaml file. 

1.) Create top level directory structure like below. I have my HDD where I store all the config and media mounted at /mnt/media
```bash
/mnt/media  
    ├── appdata
    ├── downloads
    ├── movies
    ├── music
    ├── pictures
    └── tv_shows
```
<br>

2.) Create config directories for each service like below with in the `appdata` directory
```bash
/mnt/media/appdata
    ├── jackett
    ├── lidarr
    ├── plex
    ├── radarr
    ├── sonarr
    ├── tautulli
    └── transmission-openvpn
```

3.) Clone this repo
```bash
git clone https://github.com/thundermagic/rpi_media_centre.git
cd rpi_media_centre
```

4.) Modify `docker-compose.yaml`  
Open this file with your text editor and edit the relevant parts. Comments within the file guide you what needs to be modified.
Please read all the comments. They explain a lot of stuff. Do not skip this step. 

5.) Run the services
```bash
docker-compose up -d
```

6.) Check containers are running
```bash
docker container ls -a
```
All the containers should show as running. If there is any container stuck in a reboot a cycle, check the directory 
structure created in previous steps and check container logs for more info.

##### How do I check container logs?
```bash
docker container logs <container_name>
```
Example, if you have to check logs for plex
```bash
docker container logs plex
```

If you have to follow/tail logs use the `-f` flag, example;
```bash
docker container logs -f plex
```

Assuming everything went alright, you should have all the servics running now.  
You can now access each of the services.

#### How to check if Openvpn is working?
You would need to check two things, if the tunnel interface is created and if the vpn is up and passing traffic.

For the first one, tunnel interface, on the host, check if there is a `tun` interface created when transmission-openvpn container is running. 

To check if VPN is up and passing traffic, on the host, just check your public IP by googling `whatsmyip`. If you are using the host headless, then type
`curl www.httpbin.org/get` on the console and check the IP address in the `origin` field in the output. That is the public IP being used my the host. 
Now if you check the Public IP being used by your network, that should be different from what you got from the previous step.

## Accessing services
Each service have a different port number. Assuming your RPi IP address is 192.168.4.4 and you haven't change the port 
numbers in `docker-compose.yaml` file, you can access the service like;

- Plex: http://192.168.4.4:32400/web/index.html#
- radarr: http://192.168.4.4:7878/
- sonarr: http://192.168.4.4:8989/
- lidarr: http://192.168.4.4:8686/
- transmission: http://192.168.4.4:9091/transmission/web/
- jackett: http://192.168.4.4:9117

All the port numbers are listed in the `docker container ls` command under `PORTS` column

## How do I configure services?
So you have got all the services up and running but don't know what to do next.
Check out videos from [Techno Dad Life youtube channel](https://www.youtube.com/channel/UCX2Vhc0LIzSS9aMzhGFZ7PA).  
These videos show you how to install and configure the service on openmediavault but you can just skip straight to the configuration part.

## Services details
#### Plex
This is the main media server.  
Website: www.plex.tv  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/plex

I haven't used the [official plex docker image by plexinc](https://hub.docker.com/r/plexinc/pms-docker) because its not available for `armhf` architecture.
If you are not using this media centre service on raspberry pi (basically on `armhf`), you can use this official image. 
You would need to modify `docker-compose.yaml` file accordingly.

#### Radarr
Manages and monitors movies.  
Website: https://radarr.video/  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/radarr

#### Sonarr
Manages and monitors TV shows.  
Website: https://sonarr.tv/  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/sonarr

#### Lidarr
Manages and monitors music.  
Website: https://lidarr.audio/  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/lidarr

#### Jackett
Indexer proxy.  
Website: https://github.com/Jackett/Jackett  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)  
Docker image and documentation: https://hub.docker.com/r/linuxserver/jackett

#### Transmission-openvpn
This is a single docker container running transmission and openvpn. Transmission runs only when openvpn is connected.  
Website: https://github.com/haugene/docker-transmission-openvpn  
Docker image: https://hub.docker.com/r/haugene/transmission-openvpn  
Documentation: https://haugene.github.io/docker-transmission-openvpn/

#### Tautulli
Monitors plex media server.  
Website: https://tautulli.com/  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/tautulli

#### sonarr_netimport
Fetches TV shows from a user's list from TVDB.com and add them to sonarr. I created this just because sonarr at present does not
support netimport lists.  
Website: https://github.com/thundermagic/sonarr_netimport  
Docker image and documentation: https://hub.docker.com/r/thundermagic/sonarr_netimport

#### radarr_netimport
Similar to sonarr_netimport but for radarr. Radarr has this feature built-in but radarr uses TMDB API v3 and 
I have noticed that if using v3 API, TMDB only returns maximum of 500 movies in the list. 
This is resolved if using TMDB API v4.
Website: https://github.com/thundermagic/radarr_netimport
Docker image and documentation: https://hub.docker.com/r/thundermagic/radarr_netimport

## How to upgrade a service?
When there is a new version of service available, like a newer plex version, you can follow these steps to upgrade

_**A bit of a side note regarding docker image tags:** Docker images naming conventions is `<image name>:<tag>`. Usually 
images have a `latest` tag that would be pointing to the latest version of the image. In addition to this images could 
have a tag for specific versions. Check out documentation for the image to know which tags are supported._

Assuming all the services have docker tag of `latest`, to upgrade;

`cd` into the directory where docker-compose file is.  
#### To upgrade all services
```bash
docker-compose pull
docker-compose down
docker-compose up -d
```

#### To upgrade one specific service
Taking example of the plex service which is using the container name of `plex`
```bash
docker-compose pull plex
docker container stop plex
docker container rm plex
docker-compose up -d plex
```

If a service is using specific tag, then you would need to need to change the `docker-compose.yaml` file and change the
tag to the newer tag.  
For example, assuming we have a tag of `v2` available for a service (lets call the service as `srv1` which uses the
 same name as container name)  that currently is using the tag `v1`.   
Change the tag for the image used by this service to `v2` from `v1` and then run below commands in the shell. You have
to be in the directory which have `docker-compose.yaml` file, unless you want to use the `-f` flag with `docker-compose` command.  
```bash
docker-compose pull srv1
docker container stop srv1
docker container rm srv1
docker-compose up -d srv1
```
                                                                                                                                                                  
## Do you want to monitor RPi as well?   
Check out: [Monitoring Raspberry Pi with Prometheus](https://github.com/thundermagic/rpi_monitoring_with_prometheus)                                         

## Some common issues

These are some of the issues I can think off from top of my mind that you may encounter and how to resolve them

1) **`Operation not permitted` or similar errors:** If you get these errors then the issue usually lies with either 
the user who is trying to run docker container is not a memeber of `docker` group or the user is trying to create some 
files/folder and do not have the required permissions to do so.
To resolve these, make sure the user is a member of the `docker` group. You can check this from the `/etc/group` file. 
To make a user member of docker group, type `sudo usermod -aG docker $USER` assuming you are logged in as that user. Else 
replace the `$USER` in this command with the username of the user.

2) **`Operation not supported` or `port number already used` errors:** You may get these sort of errors if something is already using
port numbers on your host that are specified for the services in the `docker-compose.yaml` file. In that case, you can change the port mappings 
for that service in the `docker-compose.yaml` file.

3) **`Device not found` or similar when running Plex container:** This error is due to the device mapping in the `docker-compose.yaml` file.
You would most likely encounter this issue if using RPi3. Please check the `docker-compose.yaml` and delete the `devices` section 
for plex.

4) **`docker-compose not found`:** You may encounter this issue after installing docker-compose because sometimes after the 
installation, the docker-compose binary is not copied to one of the paths in the $PATHS. i.e. After installation it would 
most likely be in the `$HOME/.local/bin` directory. Copy the docker-compose from here to `/usr/local/bin` directory. 
Command: `cp docker-compose /usr/local/bin`.

5) **`x-extra_args not supported` or `docker-compose version is wrong` errors:** If you get errors like this, then its an issue with
the docker-compose version. To resolve it, first change the version in the `docker-compose.yaml` file to `3.7`. If that does not
work then change it to `2`. If still it does not work, then delete the entire `x-extra_args` section and within each service definition
change the section `extra_hosts: *pi` to `extra_hosts: "pi:<HOST-IP>"` where `HOST-IP` is the IP address of the host that you are running
the services on. This just adds an entry to the `hosts` file within the container so you can use the DNS name of `pi` rather than using
ip address to connect to other services. If you are not bothered about it then you can delete this section from the container 
definition. 

## Future iterations
I am planning to run all of this on a cluster of RPis with some shared storage solution. This is something I will be working on in my
free time. Probably would run kubernetes + ceph or nfs. Haven't really thought much about it. 