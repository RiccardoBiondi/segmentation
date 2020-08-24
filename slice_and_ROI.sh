#!/bin/bash

red='\033[1;31m'
green='\033[1;32m'
reset='\033[0m]'

input_dir=$1
output_dir=$2
optional=$3


# check if the input directory exists and it is provided
if [ -z "$input_dir" ]; then

  echo -e "${red}Error! Input directory not set${reset}"
  exit 1

elif [ ! -d "$input_dir" ]; then

  echo -e "${red}Error! Input directory not found${reset}"
  exit 1

fi


# check if the output directory exists and it is provided
if [ -z "$output_dir" ]; then

  echo -e "${red}Error! Output directory not set${reset}"
  exit 1

# comment the following lines if
# the output directory could not exist
elif [ ! -d "$output_dir" ]; then

  echo -e "${red}Error! Output directory not found${reset}"
  exit 1

fi



# list all the pickle files into the input directory
input_files=$(ls $input_dir)
echo "Found ${#input_files[@]} files to process"

# define a logfile
logfile=$PWD/log_processing.txt

# eventually create the output directory
mkdir -p $output_dir

# apply the pipeline on the input files

for file in $input_files; do

  printf "* Processing $file ...       "

  f="${file%%.*}"
  python3 -m pipeline.slice_and_ROI --input=$input_dir$file --output=$output_dir$f $optional

  if [ $? = 0 ]; then
    echo -e "${green}[done]${reset}"
  else
    echo -e "${red}[failed]${reset}"
    exit 1 # you can omit this line if you want to catch
           # possible errors into the log without an exit
  fi

done
