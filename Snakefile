# snakemake --force clear               # to force rule
# snakemake --dryrun --forceall         # check workflow
# REMEMBER REMEMBER : pipe in powershell wraps the object into utf-16 char set (avoid it...evil!)
# WIN32 :=  cmd /C "snakemake --dag | dot -Tpdf > workflow.pdf"
# UNIX  :=  snakemake --dag | dot -Tpdf > workflow.pdf

# It is divided into two sections :
#   - INIT : here will be initialized the configuration file,
#            taken the filename to process and the LUNG folder, which stores
#            the files after lung extraction.
#   - RULES : here there is the implementation of the rules to perform
#             lung extraction, labelling and training.


# TODO : make a better organization of the Snakefile and confi.yaml
# TODO : find a way to reuse lung_extraction rules to prepare the training dataset
# TODO : find a way to use the input data as training data

import os
from glob import glob


# ██ ███    ██ ██ ████████
# ██ ████   ██ ██    ██
# ██ ██  ██ ██ ██    ██
# ██ ██   ████ ██    ██


configfile : "./config.yaml"

# Setting the path to the input, output and training folder. If not specified,
# the path to the training path is empty.

input_path = config['input_path']
output_path = config['output_path']
train_path = config['train_path']

#
# Glob all the file to process, both for the input and training datasets.
# Note that all the folder and files named as 'LUNG' will not be considered
# since this name is reserved to the folder that will contains the images after
# lung extraction.
#

input_files = sorted(glob(config['input_path'] + '/*'))
input_names = [os.path.basename(f) for f in input_files if os.path.basename(f) != 'LUNG']

train_files = sorted(glob(train_path + '/*'))
train_names = [os.path.basename(f) for f in train_files if os.path.basename(f) != 'LUNG']

    # ██████  ██    ██ ██      ███████ ███████
    # ██   ██ ██    ██ ██      ██      ██
    # ██████  ██    ██ ██      █████   ███████
    # ██   ██ ██    ██ ██      ██           ██
    # ██   ██  ██████  ███████ ███████ ███████

rule all :
    input :
        in_ = expand(os.path.join(output_path, "{name}.nrrd"), name = input_names)
    run :
        for file in input_names :
            old_name = os.path.join(output_path, file + '.nrrd')
            new_name = os.path.join(output_path, file.split('.')[0] + '.nrrd')
            os.rename(old_name, new_name)

rule lung_extraction :
    input :
        in_ = os.path.join(input_path, "{name}" )
    output :
        out = os.path.join(input_path, "LUNG", "{name}_lung.nrrd")
    params :
        dir = os.path.join(input_path, "LUNG")
    threads :
        config['threads_lung_extraction']
    resources :
        memory = config['memory_lung_extraction']
    shell :
        "mkdir -p '{params.dir}' | CTLungSeg/lung_extraction.py --input='{input.in_}' --output='{output.out}'"

rule prepare_train_data :
    input :
        in_ = os.path.join(train_path, "{sample}" )
    output :
        out = os.path.join(train_path, "{sample}_lung.nrrd")
    threads :
        config['threads_lung_extraction']
    resources :
        memory = config['memory_lung_extraction']
    shell :
        "CTLungSeg/lung_extraction.py --input='{input.in_}' --output='{output.out}'"


rule labelling :
    input :
        in_ = os.path.join(input_path, "LUNG","{name}_lung.nrrd"),
        center = config["centroid_path"]
    output :
        out = os.path.join(output_path, "{name}.nrrd")
    threads :
        config['threads_labelling']
    resources :
        memory = config['memory_labelling']
    log :
        "LOG/{name}.log"
    shell :
        "CTLungSeg/labeling.py --input='{input.in_}' --centroids='{input.center}' --output='{output.out}'"

rule move2lungfolder :
    input :
        in_ = expand(os.path.join(train_path, '{sample}_lung.nrrd'), sample = train_names)
    output :
        out = directory(os.path.join(train_path, 'LUNG/'))
    shell :
        "mkdir -p {output.out} | mv {input.in_} {output.out}"

rule train :
    input :
        in_ = os.path.join(train_path, 'LUNG/')
    output :
        out = config['centroid_path']
    params :
        init = config['centroid_initialization'],
        n_sub = config['n_subsamples']
    resources :
        memory = config['memory_train']
    shell :
        "CTLungSeg/train.py --input='{input.in_}' --init='{params.init}' --n={params.n_sub}--output='{output.out}'"
