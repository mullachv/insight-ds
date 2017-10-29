from extras.utils import *
from augmented_node import AugTreeNode
from collections import defaultdict

class Recipient(object):
    def __init__(self):
        self.ncontribs = 0
        self.cmte_id = ''

        #By zip
        self.ncontribs_by_zip = defaultdict(int) #num of contribs by zip
        self.contrib_amts_by_zip = defaultdict(float) #amount of contrib by zip
        self.contributions_by_zip = {} #augmented tree

        #By date
        self.ncontribs_by_date = defaultdict(int)
        self.contrib_amts_by_date = defaultdict(int)
        self.contributions_by_date = {} #augmented tree

    def update(self, rec):
        if rec:
            c, z, a, d = rec['cmte_id'], rec['zip_code'], rec['transaction_amt'], rec['transaction_dt']
            self.cmte_id = c
            self.ncontribs += 1
            if is_valid_zip(z):
                z = cleansed_zip(z)
                self.ncontribs_by_zip[z] += 1
                self.contrib_amts_by_zip[z] += a
                if z in self.contributions_by_zip:
                    self.contributions_by_zip[z].insert(a)
                else:
                    self.contributions_by_zip[z] = AugTreeNode(a)

            if is_valid_date(d):
                self.ncontribs_by_date[d] += 1
                self.contrib_amts_by_date[d] += a
                if d in self.contributions_by_date:
                    self.contributions_by_date[d].insert(a)
                else:
                    self.contributions_by_date[d] = AugTreeNode(a)


    def print_data_byzip(self, zip_code):
        if is_valid_zip(zip_code):
            zip_code = cleansed_zip(zip_code)
            if zip_code not in self.contributions_by_zip:
                return ""

            return self.cmte_id + "|" + zip_code + "|" +  \
                   str(int(round(self.contributions_by_zip[zip_code].median()))) \
                   + "|" + str(self.ncontribs_by_zip[zip_code]) + "|" + \
                   str(int(round(self.contrib_amts_by_zip[zip_code]))) \
                   + "\n"
        raise ValueError('Invalid Zip code')

    def print_data_bydate(self, dt):
        if dt not in self.contrib_amts_by_date:
            return ""

        return self.cmte_id + "|" + dt + "|" + \
            str(int(round(self.contributions_by_date[dt].median()))) \
            + "|" + str(self.ncontribs_by_date[dt]) + "|" + \
            str(int(round(self.contrib_amts_by_date[dt]))) \
            + "\n"

#Unit tests
import unittest
class TestRecp(unittest.TestCase):
    def test_3(self):
        sol = Recipient()
        rec = {
            'cmte_id': 'C00177436',
            'zip_code': '30004',
            'transaction_dt': '03212017',
            'transaction_amt': 0.9,
            'other_id': ''
        }
        sol.update(rec)
        self.assertEqual("", sol.print_data_bydate('04252017'))
    def test_2(self):
        sol = Recipient()
        rec = {
            'cmte_id': 'C00177436',
            'zip_code': '30004',
            'transaction_dt': '03212017',
            'transaction_amt': 0.9,
            'other_id': ''
        }
        sol.update(rec)
        self.assertRaises(ValueError, sol.print_data_byzip, '0321')
    def test_1(self):
        sol = Recipient()
        rec = {
            'cmte_id': 'C00177436',
            'zip_code': '30004',
            'transaction_dt': '03212017',
            'transaction_amt': 0.9,
            'other_id': ''
        }
        sol.update(rec)
        self.assertEqual("C00177436|30004|1|1|1\n", sol.print_data_byzip('30004'))


if __name__ == '__main__':
    unittest.main()
