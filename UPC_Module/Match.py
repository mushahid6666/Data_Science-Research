__author__ = 'mushahidalam'

class UPN():
    def __init__(self):{}

    def UPN_check(self,UPC_walmart,UPC_vendor):
        # UPC_walmart = UPC_walmart[2:-2]
        # UPC_vendor = UPC_vendor[2:-2]
        UPC_walmart = UPC_walmart.lstrip("0")
        UPC_vendor = UPC_vendor.lstrip("0")
        if UPC_walmart==UPC_vendor:
            return 1
        # print(UPC_walmart,UPC_vendor)
        temp = UPC_walmart[:-1]
        if temp == UPC_vendor:
            return 1
        temp = UPC_vendor[:-1]
        if UPC_walmart == temp:
            return 1

        temp = UPC_walmart[:-1]
        if len(temp) < len(UPC_vendor):
            temp = '9'+temp
            if temp==UPC_vendor:
                return 1
        temp = 'I'+UPC_walmart
        if temp==UPC_vendor:
            return 1
        return 0
# Module check code
# upn_check = UPN()
# print(upn_check.UPN_check("0012","12"))



