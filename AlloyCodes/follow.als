//	Users follow users
//	A user cannot follow themselves

sig user{
	follow : set user
}
pred show{
	all u : user | u not in u.follow
}

run show for 5
