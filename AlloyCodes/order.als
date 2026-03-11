//	Customers place orders
//	A customer may place many orders
//	Each order belongs to one customer

sig customer{
	order : set Order
}

sig Order{}

pred show{
	all o : Order | one order.o  
}
run show for 5
