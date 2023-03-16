
i
m
p
o
r
t
 
a
r
g
p
a
r
s
e


f
r
o
m
 
r
e
p
o
 
i
m
p
o
r
t
 
R
e
p
o
M
a
n
a
g
e
r




d
e
f
 
m
a
i
n
(
r
e
p
o
_
o
w
n
e
r
,
 
r
e
p
o
_
n
a
m
e
)
:


 
 
 
 
m
a
n
a
g
e
r
 
=
 
R
e
p
o
M
a
n
a
g
e
r
(
r
e
p
o
_
o
w
n
e
r
,
 
r
e
p
o
_
n
a
m
e
)


 
 
 
 
m
a
n
a
g
e
r
.
g
e
n
e
r
a
t
e
_
c
o
m
m
e
n
t
s
_
f
o
r
_
f
u
n
c
t
i
o
n
s
(
)




i
f
 
_
_
n
a
m
e
_
_
 
=
=
 
"
_
_
m
a
i
n
_
_
"
:


 
 
 
 
p
a
r
s
e
r
 
=
 
a
r
g
p
a
r
s
e
.
A
r
g
u
m
e
n
t
P
a
r
s
e
r
(
d
e
s
c
r
i
p
t
i
o
n
=
'
G
e
n
e
r
a
t
e
 
R
E
A
D
M
E
.
m
d
 
f
o
r
 
a
 
G
i
t
H
u
b
 
r
e
p
o
s
i
t
o
r
y
 
a
n
d
 
c
r
e
a
t
e
 
a
 
p
u
l
l
 
r
e
q
u
e
s
t
.
'
)


 
 
 
 
p
a
r
s
e
r
.
a
d
d
_
a
r
g
u
m
e
n
t
(
'
r
e
p
o
_
o
w
n
e
r
'
,
 
t
y
p
e
=
s
t
r
,
 
h
e
l
p
=
'
T
h
e
 
o
w
n
e
r
 
o
f
 
t
h
e
 
r
e
p
o
s
i
t
o
r
y
.
'
)


 
 
 
 
p
a
r
s
e
r
.
a
d
d
_
a
r
g
u
m
e
n
t
(
'
r
e
p
o
_
n
a
m
e
'
,
 
t
y
p
e
=
s
t
r
,
 
h
e
l
p
=
'
T
h
e
 
n
a
m
e
 
o
f
 
t
h
e
 
r
e
p
o
s
i
t
o
r
y
.
'
)


 
 
 
 
a
r
g
s
 
=
 
p
a
r
s
e
r
.
p
a
r
s
e
_
a
r
g
s
(
)


 
 
 
 
m
a
i
n
(
a
r
g
s
.
r
e
p
o
_
o
w
n
e
r
,
 
a
r
g
s
.
r
e
p
o
_
n
a
m
e
)
