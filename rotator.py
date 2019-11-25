from __future__ import print_function   # PEP 3105
import sys

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

max_bits = 32

try:
    myinput = int(raw_input("Enter the value you want to check: "))
except NameError:
    myinput = int(input("Enter the value you want to check: "))

try:
    test = xrange(0,1,2)
except NameError:
    xrange = range

print()
for n in xrange(1, 256):

    for i in xrange(0, 31, 2):

        rotated = ror(n, i, max_bits)

        if(rotated == myinput):
            print("The number %i can be used as a valid immediate number." % myinput)
            print("%i ror %x --> %s" % (n, int(str(i), 16), rotated))
            print()
            sys.exit()

else:
    print("Sorry, %i cannot be used as an immediate number and has to be split." % myinput)
