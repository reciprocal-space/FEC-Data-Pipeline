This repository constructs a pipeline to clean and extract donation data from the Federal Electoral Commission. 

More information on the project outline can be found [here](https://github.com/InsightDataScience/donation-analytics).

# Overview

The 'identifyRepeatDonors.txt' script reads each line from the database, then runs rudimentary checks to confirm each entry is valid. Once this is done, a series of more advanced checks are run, and the data is reformatted and processed if necessary. Each entry of the reprocessed data is then assigned a group based on zip code, and the group is searched to find any repeat donors. If a repeat donor is found, the script writes the entry to a final 'repeat_donors.txt' file.

A simplified workflow for the processes is shown below:

![workflow](https://raw.githubusercontent.com/reciprocal-space/FEC-Data-Pipeline/master/workflow.png)

# Execution

To run the file, locate the folder containing the './run.sh' script and execute 'bash ./run.sh'.
To run the testing suite associated with the file cd into the 'insight_testsuite' folder and run './run_tests'.

# Scalability and Performance

Two features have been considered for the future scalability and performance of this script:
1) The script reads in data line by line so that in the future analysis can be conducted on political donations, and displayed in real-time
2) The hash function is implemented to speed up processes - since the search algorithm must conduct a linear search to find repeat donors (necessitated as donations are not necessarily in order), the hash function groups each entry by zip code so that the algorithm has to search a much smaller dataset than the the full one

Performance of the script showed that the hashing algorithm needs to be optimized. When running on the full 6.7 million line FEC database, the script took too long to execute (had to be terminated prematurely) and showed a bias towards certain bins. Correcting the bias would likely add an additional speed up to the algorithm for large datasets, and could be implemented by analysing the zip-code distribution as a first step and optimizing the hash function to equally spread data between bins before sorting.

An evaluation of the speed of the script is as follows:

Input: 7 lines Speed: 0.543s
Input: 139 lines Speed: 0.840s
Input: 652 lines Speed: 1.778s

These datapoints seem to show that the script scales well with speed, although further analysis is needed to definitively say this.

# Moving Forward

Analysis of this FEC data pipeline could also provide valuable insight into the different demographics that contribute to political campaigns, and coupled with machine learning algorithms, they could be used to determine how likely a certain demographic is to be a repeat donor.
