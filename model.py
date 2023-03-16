
i
m
p
o
r
t
 
o
p
e
n
a
i


i
m
p
o
r
t
 
c
o
n
f
i
g
p
a
r
s
e
r




c
l
a
s
s
 
M
o
d
e
l
:




 
 
 
 
d
e
f
 
_
_
i
n
i
t
_
_
(
s
e
l
f
)
 
-
>
 
N
o
n
e
:


 
 
 
 
 
 
 
 
o
p
e
n
a
i
.
a
p
i
_
k
e
y
 
=
 
s
e
l
f
.
r
e
a
d
_
a
u
t
h
(
)




 
 
 
 
d
e
f
 
r
e
a
d
_
a
u
t
h
(
s
e
l
f
)
:


 
 
 
 
 
 
 
 
c
o
n
f
i
g
 
=
 
c
o
n
f
i
g
p
a
r
s
e
r
.
C
o
n
f
i
g
P
a
r
s
e
r
(
)


 
 
 
 
 
 
 
 
c
o
n
f
i
g
.
r
e
a
d
(
'
c
o
n
f
i
g
.
i
n
i
'
)


 
 
 
 
 
 
 
 
r
e
t
u
r
n
 
c
o
n
f
i
g
.
g
e
t
(
'
O
p
e
n
A
I
'
,
 
'
a
p
i
_
k
e
y
'
)


 
 
 
 


 
 
 
 
d
e
f
 
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
p
l
e
t
i
o
n
(
s
e
l
f
,
 
m
o
d
e
l
,
 
p
r
o
m
p
t
,
 
t
e
m
p
e
r
a
t
u
r
e
=
0
.
5
)
:


 
 
 
 
 
 
 
 
c
o
m
p
l
e
t
i
o
n
 
=
 
o
p
e
n
a
i
.
C
o
m
p
l
e
t
i
o
n
.
c
r
e
a
t
e
(
m
o
d
e
l
=
m
o
d
e
l
,
 
t
e
m
p
e
r
a
t
u
r
e
=
t
e
m
p
e
r
a
t
u
r
e
,
 
m
a
x
_
t
o
k
e
n
s
=
1
5
0
0
,
 
p
r
o
m
p
t
=
p
r
o
m
p
t
)


 
 
 
 
 
 
 
 
r
e
t
u
r
n
 
c
o
m
p
l
e
t
i
o
n


 
 
 
 


 
 
 
 
d
e
f
 
g
e
n
e
r
a
t
e
_
e
d
i
t
(
s
e
l
f
,
 
m
o
d
e
l
,
 
p
r
o
m
p
t
,
 
i
n
s
t
r
u
c
t
i
o
n
,
 
t
e
m
p
e
r
a
t
u
r
e
=
0
.
9
)
:


 
 
 
 
 
 
 
 
e
d
i
t
 
=
 
o
p
e
n
a
i
.
E
d
i
t
.
c
r
e
a
t
e
(
m
o
d
e
l
=
m
o
d
e
l
,
 
i
n
p
u
t
=
p
r
o
m
p
t
,
 
i
n
s
t
r
u
c
t
i
o
n
=
i
n
s
t
r
u
c
t
i
o
n
,
 
t
e
m
p
e
r
a
t
u
r
e
=
t
e
m
p
e
r
a
t
u
r
e
)


 
 
 
 
 
 
 
 
p
r
i
n
t
(
f
'
e
d
i
t
:
 
{
e
d
i
t
}
'
)


 
 
 
 
 
 
 
 
r
e
t
u
r
n
 
e
d
i
t


 
 
 
 




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
r
i
n
t
(
M
o
d
e
l
(
)
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
p
l
e
t
i
o
n
(
)
)
