from __future__ import division
__author__ = 'mushahidalam'
import json
from Search_MPN import SearchMPN
from Match import MPN
import logging

search_mpn = SearchMPN()
mpn_matcher = MPN()

class ParseJson():
    def __init__(self):{}

    def byteify(self,input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def checkMPN(self,walmart_json, vendor_json,*dict_path):
        global mpn_result
        if len(dict_path) >0:
            MPN1,MPN2,confidence = search_mpn.search_MPN(walmart_json,vendor_json,dict_path[0])
        else:
            MPN1,MPN2,confidence = search_mpn.search_MPN(walmart_json,vendor_json)
        if  MPN1=='' or MPN2=='':
            mpn_result=-1
            return -1,confidence

        mpn_result = mpn_matcher.MPN_check(MPN1,MPN2)
        return mpn_result,confidence

    def parse(self,walmart_json, vendor_json,*dict_path):
        """

        :param walmart_json:
        :param vendor_json:
        :param dict_path:
        :return:
        """
        try:
            #convert unicode to utf-8
            walmart_json = self.byteify(walmart_json)
            vendor_json = self.byteify(vendor_json)

            if(len(dict_path) > 0):
                mpn_result,confidence = self.checkMPN(walmart_json, vendor_json,dict_path[0])
            else:
                mpn_result,confidence = self.checkMPN(walmart_json, vendor_json)


            if mpn_result == -1:
                confidence =1
            Result= [mpn_result,confidence]
            return Result
        except Exception as error:
            #Error in Parsing the json file
            logging.error(error)

####Tesing Module#####
# parse_data = ParseJson()
# f = open('random_sample_elec_pairs.txt', 'r')
# for i, line in enumerate(f):
#     newlist = line.split('?')
#     walmart_json = json.loads(newlist[2])
#     vendor_json = json.loads(newlist[4])
#     print parse_data.parse(walmart_json,vendor_json,"elec_mpn_dic.txt")
