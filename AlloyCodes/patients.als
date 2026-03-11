//	Doctors treat patients
//	A doctor can treat many patients
//	A patient has exactly one doctor

sig doctor{
	treat : set patients
}
sig patients{}

pred show{
	all p : patients | one treat.p
}

run show for 5
