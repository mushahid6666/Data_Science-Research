__author__ = 'mushahidalam'
def printinfo( arg1, arg2, *dict_if_passed ):
   "This prints a variable passed arguments"
   print "Output is: "
   print arg1
   print arg2
   if(len(dict_if_passed) > 0):
       print "dict specified"
       for var in dict_if_passed:
           print var
           print dict_if_passed[0]

   else:
       print("dict not specified")
   return;

# Now you can call printinfo function
printinfo( 10 ,20)
printinfo( 70, 60, 50 )
