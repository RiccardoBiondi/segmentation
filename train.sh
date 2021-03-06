#!/bin/bash

red='\033[1;31m'
reset='\033[0m]' #No Color

input_dir=$1
output_file=$2

# check if the input directory exists and it is provided
if [ -z "$input_dir" ]; then

  echo -e "${red}Error! Input directory not set${reset}"
  exit 1

elif [ ! -d "$input_dir" ]; then

  echo -e "${red}Error! Input directory not found${reset}"
  exit 1

fi


# check if the output directory exists and it is provided
if [ -z "$output_file" ]; then

  echo -e "${red}Error! Output file not set${reset}"
  exit 1

fi

# apply the pipeline on the input files

python3 -m CTLungSeg.train --input="$input_dir" --output="$output_file" "${@:3}"
