#### What is docker container and how do I install it?
From docker.com;
> A container is a standard unit of software that packages up code and all its dependencies so the application runs 
> quickly and reliably from one computing environment to another. A Docker container image is a lightweight, 
> standalone, executable package of software that includes everything needed to run an application: code, runtime, 
> system tools, system libraries and settings.

A docker container can be thought of a process with all its dependencies coupled into a package and this package runs 
as a normal process on the host. 

##### Install docker:
```bash
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```
These steps are from: https://docs.docker.com/install/linux/docker-ce/debian/#install-using-the-convenience-script

After installation, disconnect from your host (RPi) and re-connect and check docker is installed correctly.  
After re-connecting, type `docker version` and you should get a response from like this
```bash
$ docker version
Client: Docker Engine - Community
 Version:           19.03.1
 API version:       1.40
 Go version:        go1.12.5
 Git commit:        74b1e89
 Built:             Thu Jul 25 21:33:17 2019
 OS/Arch:           linux/arm
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          19.03.1
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.5
  Git commit:       74b1e89
  Built:            Thu Jul 25 21:27:09 2019
  OS/Arch:          linux/arm
  Experimental:     true
 containerd:
  Version:          1.2.6
  GitCommit:        894b81a4b802e4eb2a91d1ce216b8817763c29fb
 runc:
  Version:          1.0.0-rc8
  GitCommit:        425e105d5a03fabd737a126ad93d62a9eeede87f
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

#### What is docker-compose and how do I install it?
Its just a simpler way of running and managing docker containers.

You need python 3 to install docker-compose.

Not sure if you already have python 3?
Just type on the console, `python3` and if you are put in the python console then you have python3 installed, if not
 follow steps to install python3. You may `python3` installed but not `python3-pip`. In that case just installed `python3-pip`,
 command `sudo apt install python3-pip`
 
##### Install python 3 and python 3 pip
```bash
$ sudo apt install python3 && sudo apt install python3-pip
```

##### Install docker-compose
```bash
$ python3 -m pip install docker-compose
```

After installation, check if docker-compose is installed correctly. Type `docker-compose version` and you should get a response
like this
```bash
$ docker-compose version
docker-compose version 1.24.1, build 4667896
docker-py version: 3.7.3
CPython version: 3.7.3
OpenSSL version: OpenSSL 1.1.1c  28 May 2019
```

##### Got error while docker or docker-compose installation?
- Check that docker isn't already installed on your host. 
- Try installation again after a reboot.
- Still not working? Try and start from clean slate, re-install the OS on SD card or try googling.
