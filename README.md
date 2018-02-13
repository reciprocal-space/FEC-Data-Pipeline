This repository contains a data pipeline constructed to clean and extract donation data from the Federal Electoral Commission. 

The goal is to identify repeat donors, so the identifyRepeatDonors.py script parses through each line of the FEC database, checking if each line is valid, and if so, it checks whether the donor has previously contributed to a political campaign

More information on the project outline can be found [here](https://github.com/InsightDataScience/donation-analytics).

# Outline

The script reads each line into the database, then runs rudimentary checks on each entry to confirm it is valid. Once this is confirmed, a series of more advanced checks is run, and the data is reformatted and processed if necessary. Each entry of the reprocessed data is then assigned a group according to its zip code, and the group is searched to find any repeat donors. If a repeat donor is found, the script writes the entry to a final 'repeat_donors.txt' file.

A simplified workflow for the processes is shown below:

![workflow](https://raw.githubusercontent.com/reciprocal-space/FEC-Data-Pipeline/master/workflow.png)

The directory structure is also as follows:


# Scalability and Performance

Two features have been considered for the future scalability and performance of this script:
1) The script reads in data line by line so that in the future, real-time analysis can be conducted on political donations, and displayed
2) The hash function is implemented to speed up processes - while the search algorithm conducts a linear search to find repeat donors, the hash function groups each entry by zip code so that the algorithm has to search a much smaller dataset than the the full one

Performance of the script showed that the hashing algorithm needs to be optimized. When running on the full 6.7 million line FEC database, the script took too long to execute (had to be terminated prematurely) and showed an bias towards certain bins. Correcting the bias would likely add an additional speed up to the algorithm for large datasets, and could be implemented by analysing the zip-code distribution and devising a hash function to equally spread data between bins.

# Moving Forward

Analysis of FEC datasets could also provide valuable insight into the different demographics that contribute to political campaigns, and coupled to machine learning algorithms, they could be used to determine how likely a certain demographic is to be a repeat donor.
