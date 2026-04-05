#include <stdio.h>

// inline function
inline int square(int x) {
    int result = x * x;
    return result;
}

int add(int a, int b) {
    int sum = a + b;
    return sum;
}

int subtract(int a, int b) {
    int diff = a - b;
    return diff;
}

int multiply(int a, int b) {
    int product = 0;
    int i;

    for(i = 0; i < b; i++) {
        product = add(product, a);
    }

    return product;
}

int factorial(int n) {
    int i;
    int fact = 1;

    for(i = 1; i <= n; i++) {
        fact = multiply(fact, i);
    }

    return fact;
}

void printArray(int arr[], int size) {
    int i;

    for(i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void processNumbers() {
    int numbers[5] = {1, 2, 3, 4, 5};
    int i;
    int sq;

    for(i = 0; i < 5; i++) {
        sq = square(numbers[i]);
        printf("Square: %d\n", sq);
    }

    printArray(numbers, 5);
}

void calculator() {
    int a = 10;
    int b = 5;
    int result1, result2, result3;

    result1 = add(a, b);
    result2 = subtract(a, b);
    result3 = multiply(a, b);

    printf("Add: %d\n", result1);
    printf("Sub: %d\n", result2);
    printf("Mul: %d\n", result3);
}

int main() {
    int num = 5;
    int fact;

    fact = factorial(num);
    printf("Factorial: %d\n", fact);

    calculator();
    processNumbers();

    return 0;
}