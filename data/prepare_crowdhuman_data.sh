#!/bin/bash

set -e

# check argument
if [[ -z $1 || ! $1 =~ [[:digit:]]x[[:digit:]] ]]; then
  echo "ERROR: This script requires 1 argument, \"input dimension\" of the YOLO model."
  echo "The input dimension should be {width}x{height} such as 608x608 or 416x256.".
  exit 1
fi

CROWDHUMAN=crowdhuman-$1

if which python3 > /dev/null; then
  PYTHON=python3
else
  PYTHON=python
fi

echo "** Install requirements"
# "gdown" is for downloading files from GoogleDrive
pip3 install --user gdown > /dev/null

# make sure to download dataset files to "yolov4_crowdhuman/data/raw/"
mkdir -p $(dirname $0)/raw
pushd $(dirname $0)/raw > /dev/null

get_file()
{
  # do download only if the file does not exist
  if [[ -f $2 ]];  then
    echo Skipping $2
  else
    echo Downloading $2...
    python3 -m gdown.cli $1
  fi
}

echo "** Download dataset files"
#get_file https://drive.google.com/uc?id=134QOvaatwKdy0iIeNqA_p-xkAhkV4F8Y CrowdHuman_train01.zip
#get_file https://drive.google.com/uc?id=17evzPh7gc1JBNvnW1ENXLy5Kr4Q_Nnla CrowdHuman_train02.zip
get_file https://drive.google.com/uc?export=download&id=1-1noaH0ZfCDiHYw2oM1pCE6EaNOyTbOj CrowdHuman_train03.zip
get_file https://drive.google.com/uc?export=download&id=1ho6apKoazy1fM4JC5PYk-nH_efsb1nli CrowdHuman_val.zip
# test data is not needed...
# get_file https://drive.google.com/uc?id=1tQG3E_RrRI4wIGskorLTmDiWHH2okVvk CrowdHuman_test.zip
get_file https://drive.google.com/u/0/uc?id=1UUTea5mYqvlUObsC1Z8CFldHJAtLtMX3 annotation_train.odgt
get_file https://drive.google.com/uc?export=download&id=1owOE8B4tohyJsnT4M5IiCUgHl1Z_vMGu annotation_val.odgt

# unzip image files (ignore CrowdHuman_test.zip for now)
echo "** Unzip dataset files"
for f in CrowdHuman_train01.zip CrowdHuman_train02.zip CrowdHuman_train03.zip CrowdHuman_val.zip ; do
  unzip -n ${f}
done
