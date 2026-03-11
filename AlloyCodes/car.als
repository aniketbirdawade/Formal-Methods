//	Cars park in slots
//	A car has exactly one slot
//	A slot has at most one car

sig car{
	park : one slot
}

sig slot{}

pred show{
	all s : slot | one park.s
}

run show for 5
