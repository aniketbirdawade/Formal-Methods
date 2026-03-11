//	People can be friends
//	Friendship is mutual
//	No one is friend with themselves

sig Pepole{
	friends : set Pepole
}
pred show{
	all p1, p2 : Pepole | p1 in p2.friends implies p2 in p1.friends
	no p: Pepole | p in p.^friends
}

run show for 5
