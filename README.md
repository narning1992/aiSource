# aiSource
adasdaasd
### Introduction
Repository for the paper ["Machine learning to predict the source of campylobacteriosis using whole genome data"](https://doi.org/10.1101/2021.02.23.432443 )

This repository should allow you to attribute sources of human campylobacter courses with the algorithm that we named **aiSource** after the previously most commonly used [iSource](https://doi.org/10.1371/journal.pgen.1000203) from core-genome multi-locus-sequence-type ([cgMLST](https://doi.org/10.1128/JCM.00080-17 )) data. The accuracy of this prediction should be ~84% based on realistic source composition in human cases. The different files in this repository do the following.

* aiSource_prediction.py - The python script allowing you to predict sources
* aiSource_classifier_object.p - A pickle object containing the XGBoost classifier trained in our paper
* test_data.tsv - a file containing test cgMLST files in a tab delimited format
* test_aiSource_out.tsv - the corresponding output file to the test data
* venv - a folder containing the virtual environment for running the python script

### Dataset acquisition
Using aiSource you can easily predict any human campylobacter cgMLST samples. Campylobacter sources can be downloaded from the fantastic [pubmlst](pubmlst.org) database. Specifically for campylobacter [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&l=1&page=query). At the bottom of the page you can export the samples using the field "Dataset" next to the Export field with the little save icon. This brings you to the Export dataset field where you can choose as many provenance fields as you want just make sure you include id and under "Schemes" you choose All loci>Typing>C. Jejuni/C. coli cgMLST v1.0 as shown below.

![Export dataset from PubMLST](./export_dataset.png)

The resulting table should be saved with "Export table(text)" and can now be used for the prediction!

If instead you want to use the dataset we used in the paper you can find it [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_isolates&page=query&project_list=102&submit=1). 

Otherwise if you have whole genomes from campy you can upload a fasta of the genome get the corresponding cgMLST patterns [here](https://pubmlst.org/bigsdb?db=pubmlst_campylobacter_seqdef&l=1&page=batchSequenceQuery). Please choose the C. jejuni. C.coli cgMLST v1.0 in the "Please select locus/scheme" menu. The resulting table should again be saved with "Export table(text)".

### Setting up the prediction


### Source attribution using aiSource

### Interpreting the output

