// Connected Graph

sig node {
  edge: set node
}

pred show {

  // no self loop
  all n: node | n not in n.edge

  // graph is connected
  all n: node | node in n.*edge
}

run show for 3
