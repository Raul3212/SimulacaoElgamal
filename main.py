from alice import *
from bob import *

# exemplo do livro (pág. 242 [pdf] = pág. 229 [livro])
# nesse exemplo x = 26, p = 29 e alpha = 2
x = 26
alice = Alice(x)
bob = Bob(29, 2)

alice.start()
bob.start()
