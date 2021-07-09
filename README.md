# aiSource
Repository for the paper "Machine learning to predict the source of campylobacteriosis using whole genome data"

## Abstract
Campylobacteriosis is among the world’s most common foodborne illnesses, caused predominantly by the bacterium Campylobacter jejuni. Effective interventions require determination of the infection source which is challenging as transmission occurs via multiple sources such as contaminated meat, poultry, and drinking water. Strain variation has allowed source tracking based upon allelic variation in multi-locus sequence typing (MLST) genes allowing isolates from infected individuals to be attributed to specific animal or environmental reservoirs. However, the accuracy of probabilistic attribution models has been limited by the ability to differentiate isolates based upon just 7 MLST genes. Here, we broaden the input data spectrum to include core genome MLST (cgMLST) and whole genome sequences (WGS), and implement multiple machine learning algorithms, allowing more accurate source attribution. We increase attribution accuracy from 64% using the standard iSource population genetic approach to 71% for MLST, 85% for cgMLST and 78% for kmerized WGS data using machine learning. To gain insight beyond the source model prediction, we use Bayesian inference to analyse the relative affinity of C. jejuni strains to infect humans and identified potential differences, in source-human transmission ability among clonally related isolates in the most common disease causing lineage (ST-21 clonal complex). Providing generalizable computationally efficient methods, based upon machine learning and population genetics, we provide a scalable approach to global disease surveillance that can continuously incorporate novel samples for source attribution and identify fine-scale variation in transmission potential


## Turtorial
### Introduction
This repository is meant to allow you to attribute sources of human campylobacter courses with the algorithm that we call **aiSource** named after the previously most commonly used iSource from cgMLST data. The accuracy of this prediction should be ~84% based on realistic source composition in human cases. The different files in this repository do the following.

* aiSource_prediction.py - The python script allowing you to predict sources
* aiSource_classifier_object.p - A pickle object containing the XGBoost classifier trained in our paper
* test_data.tsv - a file containing test cgMLST files in a tab delimited format
* test_aiSource_out.tsv - the corresponding output file to the test data
* venv - a folder containing the virtual environment for running the python script

### Dataset acquisition
Using aiSource you can easily predict any human campylobacter cgMLST samples. Campylobacter sources can be downloaded from the fantastic [pubmlst](pubmlst.org) database. Specifically for campylobacter [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&l=1&page=query). At the bottom of the page you can export the samples using the field "Dataset" next to the Export field with the little save icon. This brings you to the Export dataset field where you can choose as many provenance fields as you want just make sure you include id and under "Schemes" you choose All loci>Typing>C. Jejuni/C. coli cgMLST v1.0 as shown below.

![Export dataset from PubMLST](./export_dataset.png)

The resulting table should be saved with "Export table(text)" and can now be used for the prediction. If instead you want to use the dataset we used in the paper you can find it [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&page=query&project_list=102&submit=1). 

Otherwise if you have whole genomes from campy you can upload a fasta of the genome get the corresponding cgMLST patterns [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_seqdef&l=1&page=batchSequenceQuery). Please choose the C. jejuni. C.coli cgMLST v1.0 in the "Please select locus/scheme" menu.

### Setting up the prediction

### Source attribution using aiSource

### Interpreting the output
