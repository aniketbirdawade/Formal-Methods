//SBT
sig node{

edge: set node

}

pred show{

//Every node should have 0 or 2 children
all n:node | #n.edge=0 or #n.edge=2

//Every node has exactly one parent
all n:node | #edge.n=1
all n:node-root | #edge.n=1 and #edge.root=0

// .^ - Transitive tuple
no n:node | n in n.^edge

}

one sig root  extends node{}

run show for 5
