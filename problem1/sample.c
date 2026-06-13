int main() {
    int a, b, c, x, y, z;

    a = 1;
    b = 2;

    x = a + b;       // generates: a + b
    y = a * b;       // generates: a * b

    a = 5;           // kills all expressions using 'a': a+b, a*b

    z = a + b;       // generates: a + b  (again, after a was redefined)
    c = x * y;       // generates: x * y

    // int x,y,a,b;

    // x=a+b;
    // y=a*b;
    // while (y>a*b)
    // {
    //     a=a-1;
    //     x=a+b;
    // }
    
    
    return 0;
}