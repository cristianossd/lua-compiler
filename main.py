from sys import argv

filename = argv[1]

print "The filename: %s" % filename
f = open(filename)
code = f.read()
print code
