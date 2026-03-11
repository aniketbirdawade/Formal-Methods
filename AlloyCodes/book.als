//	Authors write books
//	An author can write many books
//	A book must have at least one author
//	A book cannot have more than 3 authors

sig Author{
	write : set Books
}

sig Books{}

pred show{
	all b : Books | some write.b

	all b : Books | #write.b <=3
}

run show for 5
