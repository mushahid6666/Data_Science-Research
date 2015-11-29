from __future__ import division
import json
import sys
import csv
from Match import UPN
from Search_UPC import SearchUPC
import logging


upc_search = SearchUPC()
upn_matcher = UPN()
class ParseJson():
    def __init__(self):{}

    def byteify(self,input):
        """
        convert unicode to utf-8
        :param input:json object
        :return:utf-8 format json object
        """
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


    def checkUPC(self,wal_json, vend_json,*dict_path):
        """
        :param wal_json: walmart json object
        :param vend_json: vendor json object
        :return:prediction: 1 (yes), 0 (no), -1 (do not know), confidence: a value in [0-1] (1 by default)
        Probe in other product if UPC field is empty or search in the dictionary provided
        """
        # Probe in other product if UPC field is empty
        # or search in the dictanory provied
        if len(dict_path) >0:
            UPC_walmart,UPC_vendor,confidence = upc_search.search_UPC(wal_json,vend_json,dict_path[0])
        else:
            UPC_walmart,UPC_vendor,confidence = upc_search.search_UPC(wal_json,vend_json)
        if UPC_walmart=='' or UPC_vendor=='':
            return -1,confidence
        upc_result = upn_matcher.UPN_check(UPC_walmart,UPC_vendor)
        return upc_result,confidence

    def parse(self,walmart_json,vendor_json,*dict_path):
        """
        :param walmart_json: Walmart Json
        :param vendor_json: Vendor Json
        :param dict_path: dictionary(optional)
        :return:
        a list of the form [prediction, confidence]
        where prediction: 1 (yes), 0 (no), -1 (do not know),
        confidence: a value in [0-1] (1 by default)(0.5 if found by probing or using dict)
        """
        try:
            #convert unicode to utf-8
            walmart_json = self.byteify(walmart_json)
            vendor_json = self.byteify(vendor_json)
            if(len(dict_path) > 0):
                upc_result,confidence = self.checkUPC(walmart_json, vendor_json,dict_path[0])
            else:
                upc_result,confidence = self.checkUPC(walmart_json, vendor_json)

            if upc_result == -1:
                confidence =1

            Result= [upc_result,confidence]
            return Result
        except Exception as error:
            #Error in Parsing the json file
            logging.error(error)

####Tesing Module#####
parse_data = ParseJson()
f = open('random_sample_elec_pairs.txt', 'r')
for i, line in enumerate(f):
    newlist = line.split('?')
    walmart_json = json.loads(newlist[2])
    vendor_json = json.loads(newlist[4])
    print parse_data.parse(walmart_json,vendor_json,"elec_upc_dic.txt")
