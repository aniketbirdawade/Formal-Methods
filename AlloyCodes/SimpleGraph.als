// Simple Graph

sig node {
  edge: set node
}
one sig head extends node{}

pred show {

  // no self loop
  all n: node | n not in n.edge
}

run show for 3
