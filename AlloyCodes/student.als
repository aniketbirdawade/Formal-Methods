//	Students sit on seats.
//	Each student has exactly one seat.
//	A seat can have at most one student.
//	There must be at least one student.

sig Students{
	sit : disj one seats
}

sig seats{}

pred show{
	all s : Students | #s.sit = 1
}

run show for 5
