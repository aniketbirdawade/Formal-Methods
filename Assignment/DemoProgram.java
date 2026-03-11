public class DemoProgram {

    // Global variable (class variable)
    static int globalNumber = 10;

    // Private variable
    private int privateNumber = 5;

    // Function to add numbers
    public int addNumbers(int a, int b) {
        int result = a + b;   // + operator
        return result;
    }

    // Function to multiply numbers
    public int multiplyNumbers(int a, int b) {
        int result = a * b;   // * operator
        return result;
    }

    // Function that uses private variable
    public void showPrivateValue() {
        System.out.println("Private Number: " + privateNumber);
    }

    public static void main(String[] args) {

        // Object creation
        DemoProgram obj = new DemoProgram();

        int x = 20;
        int y = 10;

        // Function calls
        int sum = obj.addNumbers(x, y);
        int product = obj.multiplyNumbers(x, y);

        // Printing results
        System.out.println("Global Number: " + globalNumber);
        System.out.println("Sum: " + sum);
        System.out.println("Product: " + product);

        // Call method using private variable
        obj.showPrivateValue();
    }
}