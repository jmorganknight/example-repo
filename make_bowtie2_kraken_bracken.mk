# Define the path to Bowtie2 Mouse index and the number of threads
BOWTIE2_mINDEX = /media/jmk/drive_a/Reference_Genomes/Mouse/mouse_bowtie2_index/mouse_genome_index

# Define the path to Bowtie2 Human index and the number of threads
BOWTIE2_hINDEX = /media/jmk/drive_a/Reference_Genomes/Human/human_bowtie2_index/GCA_000001405.15_GRCh38_full_analysis_set.fna.bowtie_index

THREADS_BOWTIE2 = 60

# Define the path to the Kraken 2 database and number of threads
KRAKEN2_DB = /home/jmk/kraken2/db_pluspf
THREADS_KRAKEN2 = 60

# Define path to the Bracken database
BRACKEN_DB = /home/jmk/kraken2/db_pluspf

# Define the input directory where the sample folders are located
SRC_DIR = /media/jmk/drive_a/Project_Lynn/Batch_1

# Define the output directory for Bowtie2 and Kracken2
bowtie2_mouse_output = /media/jmk/drive_a/Project_Lynn/bowtie2_2filter_output/mouse_filter
bowtie2_human_output = /media/jmk/drive_a/Project_Lynn/bowtie2_2filter_output/human_filter

# Define Kraken2 output directory for double filter
kraken2_output = /media/jmk/drive_a/Project_Lynn/kraken2_output

# Define Bracken output directory
bracken_output = /media/jmk/drive_a/Project_Lynn/bracken_output

# List of sample names (sub-folder names) in the SRC_DIR
SAMPLES = $(notdir $(wildcard $(SRC_DIR)/*))

# Define the rule to process each sample and make bracken file
all: $(foreach sample,$(SAMPLES),$(sample).bracken)

# Rule to run Kraken2
$(foreach sample,$(SAMPLES),$(sample).bracken): %.bracken: $(SRC_DIR)/%/$(SAMPLES_merged.fastq.gz)
		
	# Mouse filter: Run Bowtie2 and write unaligned reads to a file
	bowtie2 -x $(BOWTIE2_mINDEX) -p $(THREADS_BOWTIE2) -S $(bowtie2_mouse_output)/$*_output_m_bowtie2.sam -U $(SRC_DIR)/$*/$*_merged.fastq.gz --un $(bowtie2_mouse_output)/$*_not_m.fastq.gz
	
	# Human filter: Run Bowtie2 and write unaligned reads to a file
	bowtie2 -x $(BOWTIE2_hINDEX) -p $(THREADS_BOWTIE2) -S $(bowtie2_human_output)/$*_output_mh_bowtie2.sam -U $(bowtie2_mouse_output)/$*_not_m.fastq.gz --un $(bowtie2_human_output)/$*_not_m_h.fastq.gz
	
	# Run Kraken 2 on the unaligned output from Bowtie2
	kraken2 --db $(KRAKEN2_DB) --threads $(THREADS_KRAKEN2) --output $(kraken2_output)/$*_kraken2_results.txt --report $(kraken2_output)/$*_kraken2_report.txt $(bowtie2_human_output)/$*_not_m_h.fastq.gz
	
	# Run Bracken for abundance
	bracken -d $(BRACKEN_DB) -i $(kraken2_output)/$*_kraken2_report.txt -o $(bracken_output)/$*.bracken -t 20
	
	

.PHONY: all

