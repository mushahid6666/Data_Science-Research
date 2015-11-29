from __future__ import division
__author__ = 'mushahidalam'
import json

class SearchUPC():
    hashtable_upc={}

    def hashfunc(self,str1):
        #hashfunc
        hashvalue=0
        for i in range(0,len(str1)-1):
            hashvalue+=ord(str1[i])
        return hashvalue

    def searchHastable(self,product):
        #Search in Product Name
        len_limit = 12
        try:
            ProdName = product['Product Name'][0].split(' ')
            for key in ProdName:
                if len(key)<len_limit:
                    continue
                if key in self.hashtable_upc:
                    return '['+"'"+key+"'"+']'
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
                if key in self.hashtable_upc:
                    return '['+"'"+key+"'"+']'
        except:
            pass

        #search in Product Long Description
        try:
            ProdLongDesc = product['Product Long Description'][0].split(' ')
            for key in ProdLongDesc:
                key = key.lower()
                if len(key)<len_limit:
                    continue
                if key in self.hashtable_upc:
                    return '['+"'"+key+"'"+']'
        except:
            # print("parse error")
            pass
        return ''

    def __init__(self):
        #Intialize the Hastable of Possible MPN from dictonary
        for line in open("elec_upc_dic.txt", 'rw+'):
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
            str1 = str1.strip()
            hashval = self.hashfunc(str1)
            if str1 not in self.hashtable_upc:
                self.hashtable_upc[str1]= [hashval]
            else:
                # print('Append to same value')
                self.hashtable_upc[str1].append([hashval])

    def dict_init(self,dict_path):
        #Intialize the Hastable of Possible MPN from dictonary
        self.hashtable_upc.clear()
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
            str1 = str1.strip()
            hashval = self.hashfunc(str1)
            if str1 not in self.hashtable_upc:
                self.hashtable_upc[str1]= [hashval]
            else:
                # print('Append to same value')
                self.hashtable_upc[str1].append([hashval])

    def ProbeUPC(self,product,str):
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

    def search_UPC(self,wal_json,vend_json,*dict_path):
        if len(dict_path) > 0:
            self.dict_init(dict_path[0])
        dict_probe_found_UPC = 0
        mpn_found=0
        found = 0
        count=0
        try:
            UPC_walmart = wal_json['UPC']
        except:
            UPC_walmart =''#not found set it to NULL

        try:
            UPC_vendor = vend_json['UPC']
        except:
            if UPC_walmart=='':
                UPC_vendor = ''
            else:
                #Probe the UPC_walmart in Product short or long Description or Name
                if self.ProbeUPC(vend_json,UPC_walmart[0])== True:
                    UPC_vendor=UPC_walmart
                    mpn_found+=1
                    dict_probe_found_UPC = 1
                else:
                    UPC_vendor=''
        if UPC_walmart=='':
            if UPC_vendor=='':
                count+=1
            else:
                #Probe the UPC_vendor in Product short or long Description & Name
                if self.ProbeUPC(wal_json,UPC_vendor[0])== True:
                    UPC_vendor=UPC_walmart
                    mpn_found+=1
                    dict_probe_found_UPC = 1
                else:
                    UPC_walmart=''

        #search the dictonary
        if UPC_walmart=='':
            UPC_walmart = self.searchHastable(wal_json)
            if UPC_walmart!='':
                found+=1
                dict_probe_found_UPC = 1
                # print('Found in Description Walmart',found,UPC_walmart)
        if UPC_vendor=='':
            UPC_vendor = self.searchHastable(vend_json)
            if UPC_vendor!='':
                found+=1
                dict_probe_found_UPC = 1
                # print('Found in Description Vendor',found,UPC_vendor)
        # print(UPC_walmart[0],UPC_vendor[0])
        if dict_probe_found_UPC == 1:
            confidence = 0.5
        else:
            confidence = 1
        if UPC_walmart=='' and UPC_vendor=='':
            return UPC_walmart,UPC_vendor,confidence
        if UPC_walmart=='':
            return UPC_walmart,UPC_vendor[0],confidence
        elif UPC_vendor=='':
            return UPC_walmart[0],UPC_vendor,confidence
        else:
            return UPC_walmart[0],UPC_vendor[0],confidence