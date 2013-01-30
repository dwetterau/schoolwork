import os
for i in range(100):
  for j in range(10):
    myfile = file('parameters', 'w')
    print >> myfile, i/10.0
    print >> myfile, j
    myfile.close()
    print i/10.0, '-', j
    os.system('python pacman.py -l bigSearch -p ApproximateSearchAgent -z .5 -q')
