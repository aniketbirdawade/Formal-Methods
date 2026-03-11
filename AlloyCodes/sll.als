sig Node{
	next : lone Node
}

one sig head extends Node{}

pred sll{
	#next.head = 0

	all n :Node-head | #next.n=1

	no n : Node | n in n.^next

}

run sll for 3
