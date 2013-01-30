myfile = open('pacmantest','r')
num = 1
linenum = 0
max_score = -9999
for line in myfile:
    score = int(line.split()[-1])
    if score > max_score:
        max_score = score
        linenum = num
    num += 1
print "best: ", max_score, " on line ",linenum
