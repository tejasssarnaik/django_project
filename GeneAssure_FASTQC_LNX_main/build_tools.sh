#!/bin/bash

exec 3>&1
# This script installs the required tools for GeneAssure-LNX
#------------------------------------------------
RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
BLACK="\033[0;30m"
CYAN="\033[0;36m"
PURPLE="\033[0;35m"
BROWN="\033[0;33m"
WHITE="\033[1;37m"
MAGENTA='\033[0;35m'
CLEAR="\033[0m"

# Check tools installations
secho () {
	echo -e "\n${RED}$@${CLEAR}" >&3
}
CYAN="\033[0;36m"
CLEAR="\033[0m"
secho_c () {
	echo -e "\n${CYAN} $@ ${CLEAR}" >&3
}
error_call () {
	if [ ! $? -eq 0 ]; then
		currentTime=$(date "+%Y:%m:%d:%H:%M:%S")
		secho "${currentTime}: Error: $@"
		exit 1
  else
		currentTime=$(date "+%Y:%m:%d:%H:%M:%S")
		secho_c "${currentTime}:$@ completed"
	fi
}
tools_check () {
  if ! command -v $1 &>/dev/null; then
    sudo apt install $1
    error_call "$1 installation"
  else
    secho_c "$1 is previously installed"
  fi
}

# INSTALLATION PROCESS
#----------------------

if ! command -v make &>/dev/null; then
  sudo apt-get install make gcc libz-dev -y
else
  secho_c "make is previously installed"
fi

# Check if Python is installed
if command -v python3 &>/dev/null; then
  # Check Python version
  python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
  sudo ln -s /usr/bin/python3 /usr/bin/python
  secho_c "Python version: $python_version"
elif command -v python &>/dev/null; then
  # Check Python version
  python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
  secho_c "Python version: $python_version"
else
  # Install Python
  secho "Python is not installed. Installing Python..."
  sudo apt update
  sudo apt install -y python3
  python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
  secho_c "Python version: $python_version"
fi

# Installing pip
if ! command -v pip &>/dev/null; then
  sudo apt-get install -y python3-pip
  error_call "pip installation"
else
  secho_c "pip is previously installed"
fi

# Installing multiqc
if ! command -v multiqc &>/dev/null; then
  pip install -U multiqc
  error_call "multiqc installation"
else
  secho_c "multiqc is previously installed"
fi

# Installing required tools

toolsList=("tabix" "fastqc" "fastp")

for tool in "${toolsList[@]}"; do 
  tools_check $tool
done

originalDir=$(pwd)
cd ./bin/tools

cd $originalDir
exit 0