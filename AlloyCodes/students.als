//	There are students and courses.
//	A student can register for multiple courses.
//	A course must have at least one student.
//	A student cannot register for the same course twice.
//	There must be at least one course.


sig Students{
	reg : set Course
	}
sig Course{}

pred show{
	all c : Course | some reg.c
}

run show for 5
