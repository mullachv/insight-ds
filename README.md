# Insight DataScience

* Runs on Python 2.7
* Sample run command, run.sh included

## Overview
This program extracts campaign contributions by individuals and creates two files, one sorted by 
zip code and another by date. The program requirements are as specified at <a href="https://github.com/InsightDataScience/find-political-donors">InsightDataScience</a>. The input file must conform to the <a href="http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml">data dictionary<a/> published by the Federal Election Commision.
<br/><br/>
Sample output *medianvals_by_zip.txt*: 
```
C00403477|18940|459|1|459
C00403477|15237|266|1|266
C00540641|29483|300|1|300
C00540641|41601|2500|1|2500
C00540641|41601|2500|2|5000
C00003418|85266|250|23|8040
C00003418|02108|250|4|1700
```

Sample output *medianvals_by_date.txt*:
```
C00000042|01172014|230|1|230
C00000059|09042014|4900|1|4900
C00000422|01012013|1000|1|1000
C00000422|01032014|1000|3|4500
C00000422|01042013|500|5|4750
```

## Install and Run
- Clone or download this repository to a Unix (or Mac) system
- Ensure Python 2.7 is installed and available
- Execute ./run.sh
- Sample input in input/itcont.txt
- Corresponding output in output/
