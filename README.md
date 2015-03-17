I worked on quite complicated scientific project and decided to use a configuration file for model description. However it was quite complicated to parse all strings after [ConfigParser](http://docs.python.org/2/library/configparser.html) and convert every option to required Python's objects, so I would like to avoid this long/boring code as much as possible.

After several attempts, I wrote very simple parser which converts all options into Python objects by default. With some additional name resolving, I've got a simple, elegant and useful solution.

Here a small example of expanded configuration file
```
#FILE: examples.cfg

[TYPES]
int=4
float=2.5
bool=True
list=[1,2,3]
tuple=(1,5,7)
str='string'
dict={ 'a':1, 'b':2, 'c':3}
long-list=[
		1,
		2,
		3,
		4,
	]
long-dict={
		'str':'some string',
		'int':-10,
		'float': 4.,
		'bool': False,
		'list':[1,2,3,4,5]
	}
function=lambda x:x**2

[LINKS]
x = ["a","b"]
y = [ @LINKS:x@, "c"]
z = ["x"]+@LINKS:x@+["c","d"]

[COMPUTATIONS]
x = 5
y = 7
x+y = @COMPUTATIONS:x@+@COMPUTATIONS:y@
x*y = @COMPUTATIONS:x@*@COMPUTATIONS:y@
lst = range(@COMPUTATIONS:x*y@)
filter = @COMPUTATIONS:lst@[@COMPUTATIONS:x@:@COMPUTATIONS:y@]

[FUNCTIONS]
fun = lambda x: x**2+32
operation = @FUNCTIONS:fun@(12)
fun(x*y) = @FUNCTIONS:fun@(@COMPUTATIONS:x*y@)

[LINKS_AND_STRINGS]
x = "I"
y = "Python"
exmp1 = @LINKS_AND_STRINGS:x@+' love '+@LINKS_AND_STRINGS:y@
#same but with string resolving. Please not that sting inside ' '
exmp2 = '$LINKS_AND_STRINGS:x$ love $LINKS_AND_STRINGS:y$'
#BUT this will create an a problem
#exmp3 = '@LINKS_AND_STRINGS:x@ love @LINKS_AND_STRINGS:y@'
#You can resolve variable into string
exmp4 = 'In my $LINKS_AND_STRINGS:y$ + conf, $LINKS_AND_STRINGS:x$ can resolve x+y = $COMPUTATIONS:x+y$ inline'


[PARAMTERS_IN_FUNCTIONS]
#this is a parameter
parameter = 4
#to use it, include STRING into a function body
#LINK won't work!
function = lambda x: x+$PARAMTERS_IN_FUNCTIONS:parameter$

#END  examples.cfg
```

Now you can use all Python functions and objects in code:
```
>>> from confpluspy import confpluspy as cpp
>>> # Parsing file
>>> cfg = cpp("examples.cfg")
>>> 
>>> #Check all types
>>> for name  in ['int','float','bool','list','tuple','str','dict','long-list','long-dict','function']:
...  print name,"=",cfg["TYPES"][name],type(cfg["TYPES"][name])
... 
int = 4 <type 'int'>
float = 2.5 <type 'float'>
bool = True <type 'bool'>
list = [1, 2, 3] <type 'list'>
tuple = (1, 5, 7) <type 'tuple'>
str = string <type 'str'>
dict = {'a': 1, 'c': 3, 'b': 2} <type 'dict'>
long-list = [1, 2, 3, 4] <type 'list'>
long-dict = {'int': -10, 'list': [1, 2, 3, 4, 5], 'float': 4.0, 'bool': False, 'str': 'some string'} <type 'dict'>
function = <function <lambda> at 0x7feca2e0d2a8> <type 'function'>
>>> 
>>> #Check that all links have been resolved
>>> for name  in ['x','y','z']:
...  print name,"=",cfg["LINKS"][name]
... 
x = ['a', 'b']
y = [['a', 'b'], 'c']
z = ['x', 'a', 'b', 'c', 'd']
>>> 
>>> #Check that all expressions have been computed 
>>> for name  in 'x','y','x+y','x*y','lst','filter':
...  print name,"=",cfg["COMPUTATIONS"][name]
... 
x = 5
y = 7
x+y = 12
x*y = 35
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
filter = [5, 6]
>>> 
>>> #And functions work
>>> for name  in 'fun','operation','fun(x*y)':
...  print name,"=",cfg["FUNCTIONS"][name]
... 
fun = <function <lambda> at 0x7feca2e0d320>
operation = 176
fun(x*y) = 1257
>>> 
>>> #Here an example how to use string substitution ($SECTION:OPTION$)
>>> # instead of link (@SECTION:OPTION@)
>>> for name  in 'x','y','exmp1','exmp2','exmp4':
...  print name,"=",cfg["LINKS_AND_STRINGS"][name]
... 
x = I
y = Python
exmp1 = I love Python
exmp2 = I love Python
exmp4 = In my Python + conf, I can resolve x+y = 12 inline
>>> 
>>> #And now, you can use it in a code, call function for example
>>> cfg["TYPES"]["function"](2)
4
>>> 

>>> #And function with parameters
>>> cfg["PARAMTERS_IN_FUNCTIONS"]["function"](2)
6
>>> 

```

Enjoy your powerful configuration file.
