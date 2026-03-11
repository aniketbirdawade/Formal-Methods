// Strictly Binary Tree
// Node, left-right child, edge
// Apply Cardinality

sig node{edge: set node}

pred sbt{
// constraints
//every node of strictly binary tree contains exactly 0 or 2 children
// n is leader of set
// # count
// . apply only on relation
all n:node | #n.edge = 0 or #n.edge = 2
}

run sbt for 3
