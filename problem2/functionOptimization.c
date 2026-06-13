int add(int a, int b)
{
    return a + b;
}

void unused()
{
    int x = 10;
}

int factorial(int n)
{
    if(n <= 1)
        return 1;

    return n * factorial(n - 1);
}

int main()
{
    int x = add(5, 6);
    return 0;
}