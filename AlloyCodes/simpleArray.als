//	Array has indexes and values
//	Each index stores exactly one value
//	No index stores more than one value

sig Index{}
sig Value{}

sig Array{
	store :  Index -> one Value
}

pred show{

}

run show for 5
