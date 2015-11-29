from __future__ import division
__author__ = 'mushahidalam'
import json

class SearchMPN():
    hashtable_mpn={}

    def hashfunc(self,str1):
        #hashfunc
        hashvalue=0
        for i in range(0,len(str1)-1):
            hashvalue+=ord(str1[i])
        return hashvalue

    def searchHastable(self,product):
        list = []
        #Search in Product Name
        len_limit = 5
        try:
            ProdName = product['Product Name'][0].split(' ')
            for s in ProdName:
                if s == 'toner':
                    len_limit += 8
            for key in ProdName:
                key = key.lower()
                if len(key)<len_limit:
                    continue
                if key in self.hashtable_mpn:
                    list.append(key)
                    return list
        except:
            pass
        #Search in Product short description
        try:
            ProdShortDesc = product['Product Short Description'][0].split(' ')
            # print(ProdShortDesc)
            for key in ProdShortDesc:
                key = key.lower()
                if len(key)<len_limit:
                    continue
                if key in self.hashtable_mpn:
                    list.append(key)
                    return list
        except:
            pass

        #search in Product Long Description
        try:
            ProdLongDesc = product['Product Long Description'][0].split(' ')
            for key in ProdLongDesc:
                key = key.lower()
                if len(key)<len_limit:
                    continue
                if key in self.hashtable_mpn:
                    list.append(key)
                    return list
        except:
            # print("parse error")
            pass
        return ''



    def __init__(self):
        #Intialize the Hastable of Possible MPN from dictonary
        for line in open("elec_mpn_dic.txt", 'rw+'):
            line = line.rstrip('\n')
            line = line.strip()
            str1 = ''
            for i in range(len(line)-1,0,-1):
                if line[i].isspace() ==False:
                    continue
                else:
                    str1 = line[:i]
                    break
            str1 = str1.replace('\t','')
            str1 = str1.lower()
            if len(str1) <3:
                continue
            hashval = self.hashfunc(str1)
            if str1 not in self.hashtable_mpn:
                self.hashtable_mpn[str1]= [hashval]
            else:
                # print('Append to same value')
                self.hashtable_mpn[str1].append([hashval])

    def ProbeMPN(self,product,str):
        try:
            result1 = product['Product Short Description'][0].find(str)
        except:
            result1 = -1
        try:
            result2 = product['Product Long Description'][0].find(str)
        except:
            result2 = -1
        try:
            result3 = product['Product Name'][0].find(str)
        except Exception as ex:
            result3 = -1
        if result1!=-1 or result2!=-1 or result3!=-1:
            return True
        else:
            return False

    def dict_init(self,dict_path):
        self.hashtable_mpn.clear()
        #Intialize the Hastable of Possible MPN from dictonary
        for line in open(dict_path, 'rw+'):
            line = line.rstrip('\n')
            line = line.strip()
            str1 = ''
            for i in range(len(line)-1,0,-1):
                if line[i].isspace() ==False:
                    continue
                else:
                    str1 = line[:i]
                    break
            str1 = str1.replace('\t','')
            str1 = str1.lower()
            if len(str1) <3:
                continue
            hashval = self.hashfunc(str1)
            if str1 not in self.hashtable_mpn:
                self.hashtable_mpn[str1]= [hashval]
            else:
                # print('Append to same value')
                self.hashtable_mpn[str1].append([hashval])

    def search_MPN(self,wal_json,vend_json,*dict_path):
        if len(dict_path) > 0:
            self.dict_init(dict_path[0])
        dict_probe_found_MPN = 0
        mpn_found=0
        found = 0
        count=0
        try:
            MPN_Walmart = wal_json['Manufacturer Part Number']
        except:
            MPN_Walmart =''#not found set it to NULL

        try:
            MPN_Vendor = vend_json['Manufacturer Part Number']
        except:
            if MPN_Walmart=='':
                MPN_Vendor = ''
            else:
                #Probe the MPN_Walmart in Product short or long Description or Name
                if self.ProbeMPN(vend_json,MPN_Walmart[0])== True:
                    MPN_Vendor=MPN_Walmart
                    mpn_found+=1
                    dict_probe_found_MPN = 1
                else:
                    MPN_Vendor=''
        if MPN_Walmart=='':
            if MPN_Vendor=='':
                count+=1
            else:
                #Probe the MPN_Vendor in Product short or long Description & Name
                if self.ProbeMPN(wal_json,MPN_Vendor[0])== True:
                    MPN_Vendor=MPN_Walmart
                    mpn_found+=1
                    dict_probe_found_MPN =1
                else:
                    MPN_Walmart=''

        #search the dictonary
        if MPN_Walmart=='':
            MPN_Walmart = self.searchHastable(wal_json)
            if MPN_Walmart!='':
                found+=1
                dict_probe_found_MPN = 1
                # print(found,MPN_Walmart)
        if MPN_Vendor=='':
            MPN_Vendor = self.searchHastable(vend_json)
            if MPN_Vendor!='':
                found+=1
                dict_probe_found_MPN = 1
                # print(found,MPN_Vendor)
        # if type(MPN_Walmart)==

        if dict_probe_found_MPN == 1:
            confidence = 0.5
        else:
            confidence = 1
        if MPN_Walmart=='' and MPN_Vendor=='':
            return MPN_Walmart,MPN_Vendor,confidence
        if MPN_Walmart=='':
            return MPN_Walmart,MPN_Vendor[0],confidence
        elif MPN_Vendor=='':
            return MPN_Walmart[0],MPN_Vendor,confidence
        else:
            return MPN_Walmart[0],MPN_Vendor[0],confidence