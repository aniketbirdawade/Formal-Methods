// Simple Graph
sig node{
	edge: set node
}
pred show{

	// No self Loop
	all n:node | n not in n.edge

	// No Cycle
	no n:node | n in n.edge
}

run show for 5
