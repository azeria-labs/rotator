# rotator
Small script to determine valid immediate values for ARM assembly

Loading immediate values in a register on ARM is not as straightforward as it is on x86. There are restrictions on which immediate values you can use.

An ARM instruction is 32bit long, and all instructions are conditional. There are 16 condition codes which we can use and one condition code takes up 4 bits of the instruction. Then we need 2 bits for the destination register. 2 bits for the first operand register, and 1 bit for the set-status flag, plus an assorted number of bits for other matters like the actual opcodes. The point here is, that after assigning bits to instruction-type, registers, and other fields, there are only 12 bits left for immediate values, which will only allow for 4096 different values.

This means that the ARM instruction is only able to use a limited range of immediate values with MOV directly. If a number can’t be used directly, it must be split into parts and pieced together from multiple smaller numbers.

But there is more. Instead of taking the 12 bits for a single integer, those 12 bits are split into an 8bit number (n) being able to load any 8-bit value in the range of 0-255, and a 4bit rotation field (r) being a right rotate in steps of 2 between 0 and 30. This means that the full immediate value v is given by the formula: v = n ror 2*r. In other words, the only valid immediate values are rotated bytes (values that can be reduced to a byte rotated by an even number).

Here are some examples of valid and invalid immediate values:
```
Valid values:
#256        // 1 ror 24 --> 256
#384        // 6 ror 26 --> 384
#484        // 121 ror 30 --> 484
#16384      // 1 ror 18 --> 16384
#2030043136 // 121 ror 8 --> 2030043136
#0x06000000 // 6 ror 8 --> 100663296 (0x06000000 in hex)

Invalid values:
#370        // 185 ror 31 --> 31 is not in range (0 – 30)
#511        // 1 1111 1111 --> bit-pattern can’t fit into one byte
#0x06010000 // 1 1000 0001.. --> bit-pattern can’t fit into one byte
```
This has the consequence that it is not possible to load a full 32bit address in one go. If you try to load an invalid immediate value the assembler will complain and output an error saying: Error: invalid constant. 

If you need to figure out if a certain number can be used as a valid immediate value, you can use this little python script called rotator.py which takes your number as an input and tells you if it can be used as a valid immediate number.
```
azeria@labs:~$ python rotator.py
Enter the value you want to check: 511

Sorry, 511 cannot be used as an immediate number and has to be split.

azeria@labs:~$ python rotator.py
Enter the value you want to check: 256

The number 256 can be used as a valid immediate number.
1 ror 24 --> 256
```
