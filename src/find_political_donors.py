# Author: V. Mullachery
# Copyright, All rights reserved
#
# Finds political donors by zip and date from Federal Election Commission's contributions
# from Individuals file. The Metadata is described here:
# http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
#
# Two output files are created: one by zip and the other by date
#
from collections import defaultdict
import operator
from extras.utils import *
from recipient import Recipient

class Solution(object):
    def __init__(self):
        self.recipients = defaultdict(Recipient)

    def parse(self, infile, byzip, bydate):
        with open(infile, 'r') as ifile, open(byzip, 'w') as byzip:
            for line in ifile:
                chk_passes, rec = \
                    self.check_input_considerations(line)
                if chk_passes:
                    self.recipients[rec['cmte_id']].update(rec)
                    if is_valid_zip(rec['zip_code']):
                        byzip.write(self.recipients[rec['cmte_id']].print_data_byzip(rec['zip_code']))

        with open(bydate, 'w') as bydate:
            for recipient in sorted(self.recipients.values(), key=operator.attrgetter('cmte_id')):
                for dt in sorted(recipient.contributions_by_date.iterkeys()):
                    bydate.write(recipient.print_data_bydate(dt))

    def check_input_considerations(self, line):
        vals = line.strip().split('|')
        rec = {
            'cmte_id': vals[0],
            'zip_code': vals[10],
            'transaction_dt': vals[13],
            'transaction_amt': float(vals[14]),
            'other_id': vals[15]
        }

        #other_id must be empty for valid records
        if rec['other_id'] is None or rec['other_id'] == '':
            #Ignore empty cmte_id
            if rec['cmte_id'] is None or rec['cmte_id'] == '':
                return False, rec
            #Ignore empty transaction_amt
            if rec['transaction_amt'] is None or rec['transaction_amt'] == '':
                return False, rec
            return True, rec
        return False, rec

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insight Find Political Donors')
    parser.add_argument('infile', help='input file')
    parser.add_argument('byzip', help='output file of donors ordered by zip')
    parser.add_argument('bydate', help='output file of donors ordered by date')
    args = parser.parse_args()

    sol = Solution()
    sol.parse(args.infile, args.byzip, args.bydate)
