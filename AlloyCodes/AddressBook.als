sig Name, Addr{}

sig Book{
	addr: Name -> Addr
}

pred show[b:Book]{
	#b.addr >1
//	some n:Name | #n.(b.addr)>1
	#Name.(b.addr)>1
}

run show for 3 but 2 Book

// Dynamic model

pred add[b, b1:Book, n:Name, a:Addr]{
	b1.addr = b.addr+n -> a
}

pred del[b, b1:Book, n:Name]{
	b1.addr = b.addr - n-> Addr
}

run add for 3 but 2 Book
