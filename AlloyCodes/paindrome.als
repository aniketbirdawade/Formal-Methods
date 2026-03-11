//	Array has indexes and values
//	Each index stores one value
//	Two indexes cannot store the same value
open util/ordering[index]
sig index{}
sig ialue{
	v : one Int
}

one sig Array{
	store : index -> one ialue
}

fact x1{
	#index = 3
	all i : index | one Array.store[i]
	
	all disj i1 , i2 : index | Array.store[i1].v != Array.store[i2].v
}

pred show{
}

run show for 3
