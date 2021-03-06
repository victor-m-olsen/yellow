# Hello!

This is the Yellow EO Toolbox. The following script and setup will be created as a docker image.

# Ubuntu setup
  * sudo apt-get update
  * sudo apt-get install otb-bin git build-essential manpages-dev libgfortran3
  * sudo apt-get upgrade
  * sudo apt full-upgrade
  * sudo apt autoremove


# Packages
  ## Anaconda
  * Get the newest link @ https://www.anaconda.com/distribution/ 
  * cd /tmp
  * curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
  * sudo bash Anaconda3-2019.10-Linux-x86_64.sh
  * source ~/.bashrc
  * cd ~
  * sudo chown cfi -R ./*
  * sudo chown cfi .conda/environments.txt
  * conda update conda
  * conda update --all
  * conda create --name yellow python=3.8
  * conda activate yellow
  * conda install -c anaconda psutil mkl numpy scipy scikit-learn cython numexpr pandas sqlite sqlalchemy pyamg
  * conda install -c conda-forge gdal matplotlib opencv shapely geopandas scikit-image pyshp proj
  * conda update --all
  * pip install sentinelsat

  * add: OTB_MAX_RAM_HINT=24000 and GDAL_CACHEMAX=16000 to ~./bashrc with appropriate ram limits.


  ## Snappy
  * cd ~
  * curl -O http://step.esa.int/downloads/7.0/installers/esa-snap_sentinel_unix_7_0.sh
  * bash esa-snap_sentinel_unix_7_0.sh
  * Yes to all defaults, set path of python env to /home/cfi/anaconda3/envs/yellow/bin/python
  * echo 'alias gpt=~/snap/bin/gpt' >> ~/.bashrc
  * echo '-Xmx16G' >> ~/snap/bin/gpt.vmoptions
  * snap --nosplash --nogui --modules --update-all


  ## Git
  * cd ~
  * git clone https://github.com/casperfibaek/yellow.git
  * git config --global user.name "johndoe"
  * git config --global user.email johndoe@example.com
  * git config --global user.password fakefakefake
  * git config --global credential.helper store
  * git config --global credential.helper wincred


  # Test
  * otbApplicationLauncherCommandLine