// SimpleGraph

sig node{
//Set - One or More
	edge: set node
}

pred show{
	all n: node | n not in n.edge
}

run show for 3
