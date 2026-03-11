//	A company has employees.
//	Every employee has at most one manager.
//	An employee cannot manage himself.
//	There must be one CEO who has no manager.
//	All employees are reachable from CEO.

sig Employee{
	manager : lone Employee
}
one sig CEO extends Employee{}

pred show{
	no CEO.manager

	all e : Employee | e not in e.manager

	Employee = CEO.*~manager
}

run show for 5
