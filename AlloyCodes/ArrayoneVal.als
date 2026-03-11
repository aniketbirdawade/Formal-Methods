//	Array has indexes and values
//	Every index stores one value
//	Array must contain at least one index

sig Index{}
sig Value{
	v : one Int
}

sig Array{
	store : Index -> one Value 
}

pred show{
	some Index

	all disj i1, i2 : Index | Array.store[i1].v != Array.store[i2].v
}

run show for 3
