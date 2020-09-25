#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]' #No Color


input_dir=$1
centroids=$2
label1_dir=$3
label2_dir=$4


# check if the input directory exists and it is provided
if [ -z "$input_dir" ]; then

  echo -e "${red}Error! Input directory not set${reset}"
  exit 1

elif [ ! -d "$input_dir" ]; then

  echo -e "${red}Error! Input directory not found${reset}"
  exit 1

fi


#chck if the centroids file is provided
if [ -z "$centroids" ]; then

  echo -e "${red}Error! Centroid file not set${reset}"
  exit 1

#check if the centroid file exist
elif [ ! -f "$centroids" ]; then

  echo -e "${red}Error ! Centroid file not found${reset}"
  exit 1

fi


# check if the  first label dirrectory exists and it is provided
if [ -z "$label1_dir" ]; then

  echo -e "${red}Error! Output directory for label 1 not set${reset}"
  exit 1

# comment the following lines if
# the output directory could not exist
elif [ ! -d "$label1_dir" ]; then

  echo -e "${red}Error! Output directory for label 1 not found${reset}"
  exit 1

fi


# check if the  first label dirrectory exists and it is provided
if [ -z "$label1_dir" ]; then

  echo -e "${red}Error! Output directory for label 1 not set${reset}"
  exit 1

# comment the following lines if
# the output directory could not exist
elif [ ! -d "$label1_dir" ]; then

  echo -e "${red}Error! Output directory for label 1 not found${reset}"
  exit 1

fi

# list all the pickle files into the input directory
input_files=$(ls "$input_dir")
echo "Found ${#input_files[@]} files to process"

# apply the pipeline on the input files

for file in $input_files; do

  printf "* Processing $file ...       "
  f="${file%%.*}"

  python3 -m CTLungSeg.labeling --input="$input_dir$file"  --centroids="$centroids" --label1="$label1_dir$f" --label2="$label2_dir$f"

  if [ "$?" = 0 ]; then
    echo -e "${green}[done]${reset}"
  else
    echo -e "${red}[failed]${reset}"
    exit 1 # you can omit this line if you want to catch
           # possible errors into the log without an exit
  fi

done
