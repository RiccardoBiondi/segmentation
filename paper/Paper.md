---
title: 'COVID-19 Lung Segmentation'
tags:
  - Chest CT
  - Python

authors:
  - name: Riccardo Biondi^[co-first author]
    orcid: 0000-0003-0872-7098
    affiliation: 1

  - name: Nico Curti^[co-first author]
    orcid: 0000-0001-5802-1195
    affiliation: 2
  - name: Enrico Giampieri
    orcid: 0000-0003-2269-2338
    affiliation: 2
  - name: Gastone Castellani
    orcid: 0000-0003-4892-925X
    affiliation: 2

affiliations:
  - name : Department of Experimental, Diagnostic and Specialty Medicine of Bologna University
    index: 1
  - name: eDIMESLab, Department of Experimental, Diagnostic and Specialty Medicine of Bologna University
    index: 2
date: 13/06/2021

bibliography: Paper.bib
---

# Summary

The `COVID-19 Lung Segmentation` project provides a novel, non-supervised and
fully automated pipeline for the semantic segmentation of ground-glass opacities(GGO)
areas in chest CT scans of patient affected by COVID-19.
The project provides the script to segment the lung, remove the vessels and
finally identify the GGO areas.

PowerShell and bash script snakemake pipeline automate the segmentation process
for several CT scans.

A full description of the pipeline can be found in the related paper: [Classification Performance for COVID Patient Prognosis from Automatic AI Segmentation—A Single-Center Study](https://www.mdpi.com/2076-3417/11/12/5438), in which is provided also an application on real data.

The work concern the identification the ground-glass opacity using this pipeline;
radiomic measurements were collected and used to predict clinically relevant
scores, with particular focus on mortality and the PREDI-CO score

# Statement of Need

COronaVirus Disease (COVID-19) has widely spread all over the world since the
beginning of 2020. It is acute, highly contagious, viral infection mainly
involving the respiratory system. Chest CT scans of patients affected by this
condition have shown peculiar patterns of Ground Glass Opacities (GGO) and
Consolidation (CS) related to the severity and the stage of the disease.

In this scenario, the correct and fast identification of these patterns is a
fundamental task. Up to now this task is performed mainly using manual or
semi-automatic techniques, which are time-consuming (hours or days) and
subjected to the operator expertise.

This project provides an automatic pipeline for the segmentation of
ground glass opacities(GGO) areas on chest CT scans of patient affected
by COVID-19. The segmentation is achieved with a colour texture, using k-means
clustering, grouping the voxel by colour and texture similarity, and
identifying the tissue corresponding to each cluster.

# Results

The pipeline performances were tested on 15 labeled chest CT scans. These scans
were segmented and validated by expert radiologist. 10 of these scans come from
the public dataset “COVID-19 CT Lung and Infection Segmentation Dataset”
published on Zenodo. Department of Diagnostic and Preventive Medicine of the
IRCCS Policlinic Sant’Orsola-Malpighi provided the remaining 82 scans.

The segmentation performances were verified using the dice, specificity, sensitivity
and precision scores. The average value and the corresponding standard deviation
at $1\sigma$ are reported in the following table.

|Dice Score|Sensitivity|Specificity|Precision|
|:--------:|:---------:|:---------:|:-------:|
|$0.67\pm 0.12$|$0.66\pm 0.15$|$0.9992\pm 0.0005$|$0.75\pm 0.20$|

# Conclusions

The proposed unsupervised-segmentation pipeline is able to approximate the gold
standard with satisfactory results. This method can be used with success as a
first segmentation method to be used as training for other, more
specific methods.
