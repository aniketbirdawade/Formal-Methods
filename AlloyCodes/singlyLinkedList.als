// Singly linked list

sig Node{
	next : lone Node
}

one sig head extends Node{
}

pred sll{
	no n: Node | n in n.^next
}

run sll for 5
