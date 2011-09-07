#!python

# data_cleaner.py
# Takes text from standard input, cleans it, then prints the cleaned text to standard out
# Example usage: python data_cleaner.py < DirtyDataFile.txt > CleanedDataFile.txt

import sys

# Get the raw data from standard input
data = sys.stdin.read()

# Remove the special characters
newdata = unicode(str(data), 'latin-1').encode('ascii', 'ignore')

# Remove bad escape characters
cleaneddata = newdata.replace('\\','')

# Send the cleaned data to standard out
print cleaneddata

