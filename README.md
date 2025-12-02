# example-repo

# Project: Metegenomic Analysis of Alzheimer Samples

Description: The provided code is a makefile that will take fastq files and generate
abundance data for all the samples. Merged fastq files are initially filtered to remove
mouse and human sequences with Bowtie2, then remaining sequences are passed to Kraken2
and Bracken to determine microbial abundance.
