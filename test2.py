#test
import re
from PorterStemmer import *
strng = "3204\r\n.T\r\n   An On-Line Program for Non-Numerical Algebra\r\n   This is a second line\r\n.W   \r\nThe goal of this program is to make a step toward te design of an automated\r\nmathematical assistant. Some requirements for such a program are: it must be\r\neasy to access, and that the result must be obtained in a reasonably short\r\ntime. Accordingly the program is written for a time-shared computer. The Q-32\r\ncomputer as System Development Corporation, Santa Monica, California, was \r\nchosen because it also had a LISP 1.5 compiler. Programming and debugging was\r\ndone from a remote teletype console at Stanford University.\r\n.B"


# f2 = open("stopwords.txt", "r")
# for stopWord in f2:
#     print(stopWord)
#     strng.replace("The", "")
# f2.close()


dic={}
dic[1]="one"
dic[2]="two"
dic[3]="three"
dic["3"]="three"

print(dic)
if "3" in dic.keys():
    print("WINNER")
else:
    print("LOSER")

