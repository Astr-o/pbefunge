## Spec

COMMAND INITIAL STACK (bot->top)RESULT (STACK)

---

- (add) <value1> <value2> <value1 + value2>

* (subtract) <value1> <value2> <value1 - value2>

- (multiply) <value1> <value2> <value1 \* value2>
  / (divide) <value1> <value2> <value1 / value2> (nb. integer)
  % (modulo) <value1> <value2> <value1 mod value2>
  ! (not) <value> <0 if value non-zero, 1 otherwise>
  ` (greater) <value1> <value2> <1 if value1 > value2, 0 otherwise>
  > (right) PC -> right
  > < (left) PC -> left
  > ^ (up) PC -> up
  > v (down) PC -> down
  > ? (random) PC -> right? left? up? down? ???
  > \_ (horizontal if) <boolean value> PC->left if <value>, else PC->right
  > | (vertical if) <boolean value> PC->up if <value>, else PC->down
  > " (stringmode) Toggles 'stringmode'
  > : (dup) <value> <value> <value>
  > \ (swap) <value1> <value2> <value2> <value1> > \$ (pop) <value> pops <value> but does nothing
  > . (output int) <value> outputs <value> as integer
  > , (output char) <value> outputs <value> as ASCII
  > /# (bridge) 'jumps' PC one farther; skips
                                          over next command
  g (get) <x> <y> <value at (x,y)>
  p (put) <value> <x> <y> puts <value> at (x,y)
  & (input int) <value user entered>
  ~ (input character) <character user entered>
  @ (end) ends program
