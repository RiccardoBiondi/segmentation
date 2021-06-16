---
title: 'COVID-19 Lung Segmentation'
tags:
  - radiomics
  - artificial-intelligence
  - machine-learning
  - deep-learning
  - medical-imaging
  - chest-CT
  - python3
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
    affiliation: 1

affiliations:
  - name : Department of Experimental, Diagnostic and Specialty Medicine of Bologna University
    index: 1
  - name: eDIMESLab, Department of Experimental, Diagnostic and Specialty Medicine of Bologna University
    index: 2
date: 15/06/2021
bibliography: Paper.bib
---

# Summary

The `COVID-19 Lung Segmentation` project provides a novel, non-supervised and
fully automated pipeline for the semantic segmentation of ground-glass opacity
(GGO) areas in chest Computer Tomography (CT) scans of patients affected by COVID-19.
In the project we provide a series of scripts and functions for the automated
segmentation of lungs 3D areas, segmentation of GGO areas, and estimation of
radiomic features.

Both PowerShell and bash scripts are provided for the scripts management.
A possible Snakemake pipeline for the whole segmentation procedure applied
to several CT scans (in a multi-processing environment) is included into
the project.

A detailed description of the whole pipeline of processing has been already discussed
in [@app11125438@], in which we have showed also the results obtained on public
datasets [@zenodo@].
In that work we proved the efficiency of the proposed unsupervised method for the
identification of GGO areas and extraction of informative radiomic features.
Radiomic features were collected and used to predict clinically relevant
scores, with particular focus on mortality and the PREDI-CO score
[@Bartoletti2020@].

# Statement of Need

COronaVirus Disease (COVID-19) has widely spread all over the world since the
beginning of 2020.
It is acute, highly contagious, viral infection mainly involving the respiratory system.
Chest CT scans of patients affected by this condition have shown peculiar patterns
of Ground Glass Opacities (GGO) and Consolidation (CS) related to the severity
and the stage of the disease.

In this scenario, the correct and fast identification of these patterns is a
fundamental task.
Up to now, this task is mainly performed using manual or semi-automatic techniques,
which are time-consuming (hours or days) and subjected to the operator expertise.

This project provides an automated pipeline for the segmentation of
GGO areas on chest CT scans of patient affected by COVID-19.
The segmentation is achieved with a color quantization algorithm, based on k-means
clustering, which groups the voxels by color and texture similarity

The pipeline performances has been tested on 15 labeled chest CT scans dataset.
These scans were segmented and validated by expert radiologist.
Ten of these scans were extracted from the public dataset
*COVID-19 CT Lung and Infection Segmentation Dataset* [@zenodo@]
published on Zenodo.
Department of Diagnostic and Preventive Medicine of the IRCCS Policlinic Sant'Orsola-Malpighi
provided others 82 scans, with the 5 labeled used for the evaluation.

We tested the segmentation performances using the dice coefficient and specificity,
sensitivity and precision scores.
The average value and the corresponding standard deviation at $1\sigma$ are reported in
the following Table.

|  Dice Score  |  Sensitivity |    Specificity   |   Precision  |
|:------------:|:------------:|:----------------:|:------------:|
|$0.67\pm 0.12$|$0.66\pm 0.15$|$0.9992\pm 0.0005$|$0.75\pm 0.20$|

The proposed unsupervised segmentation pipeline is able to approximate the gold
standard with satisfactory results.
With this work we aimed to prove that semi-supervised approaches to segmentation are promising,
as they would combine the best effort of highly trained physicians to develop true gold standard
segmentation and the expertise of data analysts to augment those segmentation in full blown models.
While the proposed pipeline is not yet at the accuracy level necessary for assisted diagnostic,
we surmise that our pipeline can be successfully used as starting point for more specific and
performing segmentation methods.

# Acknowledgments

The authors acknowledge all the members of the Department of Radiology, IRCCS Azienda
Ospedaliero-Universitaria di Bologna and the SIRM foundation, Italian Society of Medical and
Interventional Radiology for the support in the development of the project and analysis of the data.

# References
