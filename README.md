![SSAILR Logo](logo.png)

# SSAILR
This is the README document for the SSAILR pipeline for pre-processing and analyzing HTS reads from _in vitro_ selection experiments. 

# Usage


Please consult the EasyDIVER [documentation](https://github.com/ichen-lab-ucsb/EasyDIVER) for the pre-processing part of the pipeline. 

# Dependencies
The pipeline script was written to run on Unix-based systems, like Linux, Ubuntu, and MacOS. Windows 10 also has a [Linux subsystem](https://docs.microsoft.com/en-us/windows/wsl/faq).

To use the pipeline, first install the two dependencies: [Python](https://www.python.org/downloads/) and [PANDASeq](https://github.com/neufeld/pandaseq/wiki/Installation). We recommend using the Anaconda distribution of python, and adding the Bioconda channel to Anaconda's package manager, conda. See the [Anaconda documentation](https://docs.anaconda.com/anaconda/install/) for installation. After installing Anaconda with [Bioconda](https://bioconda.github.io/), PANDASeq is easily installed using conda with:

`conda install pandaseq`

In order for the pipeline to be called from any directory and for the pipeline to call the translator reliably, both scripts must be placed in a directory that is in the user's PATH environment variable upon download. For example, for Unix/Linux users, scripts could be placed in `/usr/local/bin/` upon download. These files can be placed in that directory with the command:

`cp /path/to/pipeline.sh /path/to/translator.py /usr/local/bin/` 

EasyDIVER and the translation tool must be made executable. This can be done by entering the following commands from the local directory where they are stored:

`chmod +x easydiver.sh`
`chmod +x translator.py`

The pipeline will not be found unless it is stored in the working directory or in a directory that is in the user's PATH environment (e.g. `bin/`). Also, the pipeline will not be able to find the translator if it is not stored in a directory that is in the user's PATH environment (e.g. `bin/`). 

# INPUT

All input files must be:
    
1. Located in the same directory (even reads from separate lanes).
2. In FASTQ format
3. Named using the standard Illumina naming scheme: sample-name_S#_L00#_R#_001.fastq
4. In either .fastq or .fastq.gz extensions.

### Naming scheme:

For each round of selection, files must be labeled as "R-type-X", where R is the round number, type is either in, out or neg (for input, output and negative control), and X can be any string that helps the user identify which sample it corresponds to. For example, for a 2 rounds experiment with input, output and negative control, files names should look like:

1-in-Sample1_L001_R1_001.fastq.gz\
1-in-Sample1_L001_R2_001.fastq.gz\
1-out-Sample2_L001_R1_001.fastq.gz\
1-out-Sample2_L001_R2_001.fastq.gz\
2-in-Sample3_L001_R1_001.fastq.gz\
2-in-Sample3_L001_R2_001.fastq.gz\
2-out-Sample4_S10_L001_R1_001.fastq.gz\
2-out-Sample4_S10_L001_R2_001.fastq.gz

# Test dataset

A test dataset is provided. The test data corresponds to two samples obtained from a real experiment of in vitro evolution of mRNA displayed peptides. 
     
# Reporting bugs

Please report any bugs to Celia Blanco (celiablanco@ucla.edu). 

When reporting bugs, please include the full output printed in the terminal when running the pipeline. 

If a problem is encountered with newer MacOS versions after installing PANDASeq, you may try the following:

1. Install Homebrew (see here: https://brew.sh/)
2. brew install bzip2 pkgconfig libtools
3. Run the ./autogen.sh build step (see PANDASeq manual)

If an error referencing snprintf occurs, identify the file from the error message, open that file and adjust 'snprintf' to be 'printf' instead. During our test runs, this issue was found in line 528 in the pandaseq package args.c file. 
Run the ./autogen.sh build step again. At this point, you might get many ‘warnings’ but you shouldn't get any errors. 

# Citation

TBD

