"""
Pet Weight Calculator Module
Based on formula: W = (Wh / 11) × (A + 10)
"""

class PetWeightCalculator:
    @staticmethod
    def calculate_hatch_weight(current_weight: float, current_age: int) -> float:
        """
        Calculate hatch weight from current weight and age
        Formula: Wh = (W * 11) / (A + 10)
        """
        if current_age < 1 or current_age > 100:
            raise ValueError("Age must be between 1 and 100")
        if current_weight <= 0:
            raise ValueError("Weight must be positive")
        
        hatch_weight = (current_weight * 11) / (current_age + 10)
        return round(hatch_weight, 2)
    
    @staticmethod
    def calculate_current_weight(hatch_weight: float, age: int) -> float:
        """
        Calculate current weight from hatch weight and age
        Formula: W = (Wh / 11) × (A + 10)
        """
        if age < 1 or age > 100:
            raise ValueError("Age must be between 1 and 100")
        if hatch_weight <= 0:
            raise ValueError("Hatch weight must be positive")
        
        current_weight = (hatch_weight / 11) * (age + 10)
        return round(current_weight, 2)
    
    @staticmethod
    def get_weight_class(weight: float) -> str:
        """Determine weight classification"""
        if weight < 1:
            return "Small"
        elif 1 <= weight < 5:
            return "Normal"
        elif 5 <= weight < 7:
            return "Huge"
        elif 7 <= weight < 9:
            return "Titanic"
        else:
            return "Godly"
    
    @staticmethod
    def generate_growth_table(hatch_weight: float) -> list:
        """Generate growth table from age 1 to 100"""
        growth_data = []
        for age in range(1, 101):
            current_weight = PetWeightCalculator.calculate_current_weight(hatch_weight, age)
            weight_class = PetWeightCalculator.get_weight_class(current_weight)
            growth_data.append({
                'age': age,
                'weight': current_weight,
                'class': weight_class
            })
        return growth_data

# Example usage
if __name__ == "__main__":
    # Test the calculator
    calculator = PetWeightCalculator()
    
    # Calculate hatch weight from current stats
    hatch_weight = calculator.calculate_hatch_weight(4.38, 28)
    print(f"Hatch Weight: {hatch_weight} kg")
    
    # Calculate current weight at different ages
    for age in [10, 28, 50, 100]:
        current_weight = calculator.calculate_current_weight(hatch_weight, age)
        weight_class = calculator.get_weight_class(current_weight)
        print(f"Age {age}: {current_weight} kg ({weight_class})")
