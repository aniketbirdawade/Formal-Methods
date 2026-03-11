open util/ordering[Index]
sig Index{}
sig Value{}

sig Array{
	store : Index -> one Value
}

fact x1{
	#Index = 3
	all i : Index | one Array.store[i]
	
	Array.store[first] = Array.store[last]
	Array.store[next[first]] = Array.store[prev[last]] 
}
pred show{

}
run show for 3
