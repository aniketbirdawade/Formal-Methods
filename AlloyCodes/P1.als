sig Node {
	left : lone Node, 
	right : lone Node
}

one sig Root extends Node {}
pred sbt{
	no n  : Node | n in n.^left or n in n.^right
	Node = Root.*(left+right)

	no n: Node | Root in n.(left+right)
	all n : Node | some n.left iff some n.right

	all n : Node | some n.left implies n.left != n.right
}


run sbt for 7
