import math

def main():
    try:
        # Read coefficients a, b, and c from the user.
        coefficients = input("Enter coefficients a, b, c separated by spaces: ").split()
        if len(coefficients) != 3:
            print("Please enter exactly three coefficients.")
            return
        
        a, b, c = map(float, coefficients)
        if a == 0:
            print("Coefficient a cannot be zero in a quadratic equation.")
            return
        
        # Calculate the discriminant.
        discriminant = b**2 - 4 * a * c
        
        # Compute square root, handling complex results if needed.
        if discriminant >= 0:
            sqrt_val = math.sqrt(discriminant)
        else:
            sqrt_val = complex(0, math.sqrt(-discriminant))
        
        # Calculate the two roots x0 and x1.
        x0 = (-b + sqrt_val) / (2 * a)
        x1 = (-b - sqrt_val) / (2 * a)
        
        print("x0 =", x0)
        print("x1 =", x1)
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")

if __name__ == '__main__':
    main()