//	Library has books and members.
//	A member can borrow many books.
//	A book can be borrowed by only one member at a time.
//	A member cannot borrow the same book twice.

sig Member{
	borrow : set books
}
sig books{}

pred show{
	 all b : books | lone borrow.b
}

run show for exactly 5 books,2 Member
