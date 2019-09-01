# Media Centre on Raspberry Pi
This is a bundle of different docker containers to run a media centre with additional services to run and manage your own media or use torrents. 

**DISCLAIMER: NOT ALL THE SERVICES ARE CREATED BY ME. I HAVE JUST PUT THEM TOGETHER.**

Since this uses docker container, it can be run on `amd64` platforms as well (i.e your windows or linux machine). 
This guide is generic, any platform specific changes would be highlighted with comments.

## Isn't Raspberry Pi under powered to run a media centre?
Raspberry Pi 4 actually makes a good low powered platform to run a home media centre system. It can't really handle video 
transcoding but if you are using this for home purpose and all the video clients are under your control, you can choose the
clients that would play most of the video content without transcoding (i.e direct play).

I have been using a single Raspberry Pi 4 4GB version as a media centre since the day it was launched (actually couple of days after 
the release for delivery time). Before that I was using a Raspberry Pi 3B+ and that worked alright as well.  
It would direct play few streams at the same time without any issue, assuming your home network is good enough. Wired 
connectivity between clients and the media server would help.  
My home setup is all on one RPi 4 (overclocked to 1850 MHz). For storage I have two HDD connected to the Pi and they are in RAID 1. I am using linux
software raid (mdadm). I am also running monitoring stuff on the same Pi (prometheus, grafana etc etc). There has been no performance
issues with the Raspberry Pi. I have amazon firestick 4K as video clients connected to TVs. These can play most of the video content. 
And if there is any content that requires transcoding to play, then I just get the format that would direct play on firestick. 
If I am managing video content then I can control which video formats I get. This is quite easy to do using radarr. You can exclude
video formats that you don't want.

You would need active cooling for RPi 4. It gets HOT!

Yes, if you want to transcode video and want to serve content over the WAN to friends and family, then you would need something
more powerful. You can still use this guide, it would work regardless if you are using a RPi or something else.

## Services used
#### For media server
- Plex: Main media server
- transmission: Torrent client
- Openvpn: VPN client
- radarr: Automated movie integration with torrent client
- sonarr: Same as radarr but for TV shows
- lidarr: Same as radarr but for Music
- tautulli: Plex media server monitoring service
- Jackett: Torrent indexers proxy
- sonarr_netimport: A python script to fetch TV shows from tvdb.com and add them to sonarr

Note: transmission and openvpn are in one container

## Do you want to monitor RPi as well?
Please check out: https://github.com/thundermagic/rpi_monitoring_with_prometheus

## Prerequisite 
- docker
- docker-compose

Follow this guide if you have to install docker and docker-compose: https://github.com/thundermagic/rpi_media_centre/blob/master/docs/docker_install.md

## Quick start
Ok lets start to run the media server

**NOTE:** You can change where data is stored and use your own directory structure by editing `docker-compose.yaml`. More details are in the yaml file. 

1.) Create top level directory structure like below with root being /mnt/media. I have my HDD where I store all the config and media mounted at /mnt/media
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
    ├── grafana
    ├── jackett
    ├── lidarr
    ├── plex
    ├── prometheus
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
Please read all the comments. They explain a lot of stuff.  

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

##### How to check container logs?
```bash
docker container logs <container_name>
```
Example, if you have to check logs for plex
```bash
docker container logs plex
```

If you have to follow logs use the `-f` flag, example;
```bash
docker container logs -f plex
```

Assuming everything went alright, you should have all the servics running now.  
You can now access each of the services.

## Accessing services
Each service have a different port number. Assuming your RPi IP address is 192.168.4.4, you can access the service like;

- Plex: http://192.168.4.4:32400/web/index.html#
- radarr: http://192.168.4.4:7878/
- sonarr: http://192.168.4.4:8989/
- lidarr: http://192.168.4.4:8686/
- transmission: http://192.168.4.4:9091/transmission/web/
- grafana: http://192.168.4.4:3000
- prometheus: http://192.168.4.4:9090
- jackett: http://192.168.4.4:9117

All the port numbers are listed in the `docker container ls` command under `PORTS` column

## How do I configure services?
So you have got all the services up and running but don't know what to do next.
Check out videos from [Techno Dad Life youtube channel](https://www.youtube.com/channel/UCX2Vhc0LIzSS9aMzhGFZ7PA).  
These videos show you how to install and configure the service on openmediavault but you can just skip straight to the configuration part.

## Services details
### Media centre services
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
Manages and monitors TV Shows.  
Website: https://sonarr.tv/  
Docker image by: [linuxserver.io](https://www.linuxserver.io/)   
Docker image and documentation: https://hub.docker.com/r/linuxserver/sonarr

#### Lidarr
Manages and monitors Music.  
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
support netimport lists  
Website: https://github.com/thundermagic/sonarr_netimport  
Docker image and documentation: https://hub.docker.com/r/thundermagic/sonarr_netimport








