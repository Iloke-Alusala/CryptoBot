

errorDelim = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
buyDelim =   "/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/"
sellDelim =  "\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\"
startDelim = ".--.--.--.--.--.--.--.--.--.--.--.--.--"
tfName = "CryptoLogging(Day4).txt"

tf = open(tfName, "r")
newLog = ""

lines = tf.readlines()
firstBlock = False
startBlock = False
block  = ""
unique = set()

for i in range(len(lines)):
    if((lines[i] == errorDelim+"\n") or (lines[i]==buyDelim+"\n") or (lines[i]==sellDelim+"\n") or (lines[i]==startDelim+"\n")):
        startBlock = not(startBlock)
        firstBlock = True
    if(startBlock and firstBlock):
        block += lines[i]

    if(not(startBlock) and firstBlock):
        unique.add(block)

for
        
        
'''
