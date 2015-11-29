__author__ = 'mushahidalam'
import re
class MPN():
    color_dict_mpn = []

    def __init__(self):{}

    def dict_gen(self):
        filename = 'color_dict.txt'
        for line in open(filename, 'rw+'):
            line = line.rstrip('\n')
            self.color_dict_mpn.append(line)

    def hasNumbers(self,inputString):
        lent = len(inputString)
        if len==1:
            return True
        else:
            return False
        # return any(char.isdigit() for char in inputString)

    def MPN_check(self,product1,product2):
        self.dict_gen()
        # if json_or_csv==1:
        mpn_1 = product1
        mpn_2 = product2
        # print(mpn_1,mpn_2)
        mpn_1 = mpn_1.upper()
        mpn_2 = mpn_2.upper()

        #intial test if string match by removing hyphen
        copy1 = mpn_1[:]
        copy2 = mpn_2[:]
        test1 = copy1.replace('-','')
        test2 = copy2.replace('-','')
        # print(str(test1),type(test1),str(test2),type(test2))
        if str(test1) == str(test2):
            # print("returning 1 62")
            return 1

        #check if only one of string contains hyphen
        copy1 = str(mpn_1)
        copy2 = str(mpn_2)
        test1 = copy1.find('-')
        if test1!=-1:
            test2 = copy2.find('-')
            if test2==-1:
                copy1 = copy1.split('-')
                if copy1[0] ==copy2:
                    return 1

        copy1 = str(mpn_1)
        copy2 = str(mpn_2)
        test1 = copy2.find('-')
        if test1!=-1:
            test2 = copy1.find('-')
            if test2==-1:
                copy2 = copy2.split('-')
                if copy1 ==copy2[0]:
                    return 1

        hyphenmpn1 = mpn_1.find('-')
        hyphenmpn2 = mpn_2.find('-')
        if hyphenmpn1 !=-1:
            if hyphenmpn2!=-1:
                list = mpn_1.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_1 = mpn_1.replace(list[lent-1],'')
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_1 = mpn_1.replace(list[lent-1],'')
                list = mpn_2.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_2 = mpn_2.replace(list[lent-1],'')
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_2 = mpn_2.replace(list[lent-1],'')
            else:
                list = mpn_1.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_1 = mpn_1[:-1]
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_1 = mpn_1.replace(list[lent-1],'')

        if hyphenmpn2 !=-1:
            if hyphenmpn1!=-1:
                list = mpn_1.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_1 = mpn_1.replace(list[lent-1],'')
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_1 = mpn_1.replace(list[lent-1],'')
                list = mpn_2.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_2 = mpn_2.replace(list[lent-1],'')
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_2 = mpn_2.replace(list[lent-1],'')
            else:
                list = mpn_2.split('-')
                lent = len(list)
                if self.hasNumbers(list[lent-1]):
                    mpn_2 = mpn_2[:-1]
                else:
                    for i in self.color_dict_mpn:
                        if i == list[lent-1]:
                            mpn_2 = mpn_2.replace(list[lent-1],'')
        mpn_1 = mpn_1.strip()
        mpn_2 = mpn_2.strip()
        #remove trailing hyphens
        lent = len(mpn_1)
        if mpn_1[lent-1] == '-':
            mpn_1 = mpn_1[:-1]
        lent = len(mpn_2)
        if mpn_2[lent-1] == '-':
            mpn_2 = mpn_2[:-1]
        result = mpn_1.find('-')
        if result!=-1:
            list = mpn_1.split('-')
            lent = len(list)
            if self.hasNumbers(list[lent-1]):
                mpn_1 = mpn_1.replace(list[lent-1],'')
        result = mpn_2.find('-')
        if result!=-1:
            list = mpn_2.split('-')
            lent = len(list)
            if self.hasNumbers(list[lent-1]):
                mpn_2 = mpn_2.replace(list[lent-1],'')
        mpn_1 = mpn_1.replace('-','')
        mpn_2 = mpn_2.replace('-','')
        if mpn_1== mpn_2:
            # print(mpn_1,mpn_2,1)
            return 1
        else:
            # print(mpn_1,mpn_2,0)
            return 0
        # else:
        #     mpn_1 = product1['Manufacturer Part Number']
        #     mpn_2 = product2['Manufacturer Part Number']
        #     mpn_1 = mpn_1[0]
        #     mpn_2 = mpn_2[0]
        #     mpn_1 = mpn_1.replace('-','')
        #     mpn_2 = mpn_2.replace('-','')
        #     if mpn_1== mpn_2:
        #         result1 = 1
        #     else:
        #         result1 = 0
        #     self.dict_gen()
        #     if(result1==1):
        #         return 1
        #     return 0


# Module testing
# mpn_module = MPN()
# product1 ='3200'
# product2 ='3200'
# result = mpn_module.MPN_check(product1,product2,1)

