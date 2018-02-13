# The following code cleans donation data from the Federal Electoral Commission, and searches for repeat donors.
# The code is strucured to read in data one line at a time, so as to provide scalability for the future.
#

import pandas as pd
import numpy as np
import string
import dateutil
import sys

def mainFunctionz(inputFile, percentileFile, outputFile):
    count = 0
    amounts_list = []    
    error_counter = 0
    total_amount = 0
    x=0
    recordsProcessed = 0
    #colnames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't' 'u']

    for df in pd.read_csv(inputFile, sep="|", header=None, chunksize = 1, dtype={10 : object}):
        cmteID = df.iloc[x,0]
        name = df.iloc[x,7]
        zipCode = df.iloc[x,10]
        transDT = df.iloc[x,13]
        transAMT = df.iloc[x,14]
        otherID = df.iloc[x,15]
        recordsProcessed = recordsProcessed + 1

        print "Entry:", cmteID, name, zipCode, transDT, transAMT, otherID
        #checks if any basic fields are empty
        result = rudimentaryChecks(otherID, cmteID, zipCode, transAMT)
        if result == False:
            error_counter = error_counter + 1
            pass
        else:
            #checks if zipcode is valid, invalid, or needs to be shortened
            zip = testZipCode(zipCode)
            #checks if name consists of valid characters
            nameTester = testName(name)
            #checks if transaction date is valid
            testTransDate = testTransactionDate(transDT)

            if (zip == False) or (nameTester == False) or (testTransDate == False):
                error_counter = error_counter + 1
                pass
            else:
                print "All fields are valid"
                #calculates a group for each entry based on zip code
                grouping = int(zip) % 11
                #writes each entry into a group, and checks for repeat donors
                match, line = hashFunction(grouping, zip, nameTester, transAMT, transDT, cmteID)
                #extracts percentile from file
                percentile = get_percentile(percentileFile)
                
                #hashFunction() successfully found a repeat donor
                if match == 1:
                   count = count + 1
                   amounts_list.append(transAMT)
                   amounts_list.sort()
                   #calculates the nth percentile of the data using the nearest-rank method
                   percentile_value = np.percentile(amounts_list, percentile, interpolation='nearest')
                   total_amount = total_amount + transAMT
                   print "We got one!"
                   print cmteID, name, zip, transAMT, amounts_list, percentile_value, total_amount
                   #writes the entry to the repeat_donor.txt
                   writeFinalFile(cmteID, zip, testTransDate[-4:], percentile_value, total_amount, count, outputFile)
                   print "Successfully written to repeat_donors.txt \n"
                #hashFunction() successfully found a match but the dates are not in order
                elif match == 'seven':
                   entry = line.split()
                   print "Dates out of order, using earlier entry", entry[0], entry[1], entry[2], entry[3], entry[4]
                   count = count + 1
                   date = str(entry[4])
                   dollas = int(entry[3])
                   amounts_list.append(dollas)
                   amounts_list.sort()
                   #calculates the nth percentile of the data using the nearest-rank method
                   percentile_value = np.percentile(amounts_list, percentile, interpolation='nearest')
                   total_amount = total_amount + dollas
                   print entry[0], entry[1], entry[2], entry[3], entry[4]
                   writeFinalFile(entry[0], entry[1], date[-4:], percentile_value, total_amount, count, outputFile)
                   print "Successfully written to repeat_donors.txt \n"
                else:
                    error_counter = error_counter + 1
                    print "No match found\n"
                    pass

    print "Repeat donors:", count, " One-time donors: ", error_counter
    print "Records processed: ", recordsProcessed
    return


def rudimentaryChecks(otherID, cmteID, zipCode, transAMT):
    if pd.isnull(otherID) == False:
        print "Error: other_ID is not empty\n"
        return False
    elif pd.isnull(cmteID) == True:
        print "Error: cmte_ID is empty\n"
        return False
    elif pd.isnull(zipCode) == True:
        print "Error: zip_code is empty\n"
        return False
    elif pd.isnull(transAMT) == True:
        print "Error: transaction_amount is empty\n"
        return False
    else:
        print "Rudimentary checks passed"
        return True

def testZipCode(zippityzip):
    dummy = str(zippityzip)
    i = 0
    n = i + 5
    if dummy.isdigit() == True:
        if len(dummy) == 0:
            print "Error: zip_code is empty\n"
            return False, error_counter
        elif len(dummy) > 5:
            return dummy[0:5]
        elif len(dummy) < 5:
            print "Error: zip_code is not valid (less than five digits)\n"
            return False
        elif len(dummy) == 5:
            return dummy
        else:
            print "Error: zip_code is not valid\n"
            return False
    else:
        print "Error: zip_code is malformed\n"
        return False

def testName(name):
    dummy = str(name)
    table = string.maketrans("","")
    dumdum = dummy.translate(table, string.punctuation)
    dumdumdum = dumdum.replace(" ", "")

    if dumdumdum.isalpha() == True:
        return dumdumdum
    else:
        print "Error: name is malformed\n"
        return False

def testTransactionDate(transDate):
    dummm = str(transDate)

    try:
        bumm = dateutil.parser.datetime.datetime.strptime(dummm, '%m%d%Y')
        return dummm
    except ValueError:
        print "Error: invalid transaction_date\n"
        return False

def hashFunction(grouping, zip, parsedName, transAMT, transDT, cmteID):
    fileName = str(grouping) + ".txt"
    output = str(cmteID) + " " + str(zip) + " " + str(parsedName) + " " + str(transAMT) + " " + str(transDT) + "\n"
    check = output.split()
    match = None
    print "Writing entry to ", fileName

    with open(fileName, "a+") as f:
        for line in f:
            print "Checking if", output, " and entry ", line, " match"
            if check[1] == line.split()[1] and check[2] == line.split()[2]:
                if check[-2] < line.split()[-2]:
                    match = 'seven'
                    return match, line
                else:
                     match = 1
                     return match, None
            else:
                match = 0
                print "Not a match"
        f.write(str(output))
    return match, None

def get_percentile(percentileFile):
    percentile = None
    with open(percentileFile, 'r') as file:
        for element in file:
            percentile = element
    return percentile[0:2]

def writeFinalFile(cmteID, zip, date, percentile, total, count, outputFile):
    with open(outputFile, 'a+') as f:
        f.write(str(cmteID) + "|" + str(zip) + "|" + str(date) + "|" + str(percentile) + "|" + str(total) + "|" + str(count) + "\n")
    return

if __name__ == '__main__':
    mainFunctionz(sys.argv[1], sys.argv[2], sys.argv[3])
