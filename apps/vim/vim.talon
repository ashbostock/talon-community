os: mac
app: vi
app: vim
-

drop:
    key(escape)
    insert(":%s/pick/drop/gci\n")

squash:
    key(escape)
    insert(":%s/pick/squash/gci\n")

clean commit:
    key(escape)
    key(d:6)
    key(escape)
    key(down)
    key(d:8)

insert [<phrase>]:
    key(escape)
    key(i)
    insert(phrase or "")

append [<phrase>]:
    key(escape)
    key(a)
    insert(phrase or "")

replace [<phrase>]:
    key(escape)
    key(shift-r)
    insert(phrase or "")

line start:
    key(escape) 
    key(0)
line end: 
    key(escape)
    key($)
line cut:  
    key(escape)
    key(d:2)
line copy: 
    key(escape)
    key(y:2)
paste:
    key(escape)
    key(p) 
paste above:
    key(escape)
    key(shift-p)

save:
    key(escape)
    insert(":x")

close:
    key(escape)
    insert(":q!")

undo: 
    key(escape)
    key(u)
redo: 
    key(escape)
    key(ctrl-r)