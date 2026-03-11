//	Teachers teach courses
//	A teacher may teach many courses
//	A course has exactly one teacher

sig Teacher{
	teaches : set course
}

sig course{}

pred show{
	all c : course | one teaches.c
}

run show for 5
