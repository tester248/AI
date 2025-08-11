class Item:
    def __init__(self, item_id, weight, value):
        self.item_id = item_id
        self.weight = weight
        self.value = value

def create_items():
    items = []
    n = int(input("Enter number of items: "))
    for i in range(n):
        item_id = input(f"Enter item ID for the item {i+1}: ")
        weight = int(input(f"Enter weight of the item {i+1}: "))
        value = int(input(f"Enter profit/value of the item {i+1}: "))
        print()
        items.append(Item(item_id, weight, value))
    return items

def solve_knapsack_zero_one(capacity, items):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item_weight = items[i-1].weight
        item_value = items[i-1].value

        for w in range(1, capacity + 1):
            if item_weight > w:
                dp[i][w] = dp[i-1][w]
            else:
                value_if_not_included = dp[i-1][w]
                value_if_included = item_value + dp[i-1][w - item_weight]
                dp[i][w] = max(value_if_not_included, value_if_included)

    total_value = dp[n][capacity]

    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(items[i-1])
            w -= items[i-1].weight

    return total_value, selected_items

def solve_knapsack_fractional(capacity, items):
    #sort by value per weight ratio
    items.sort(key=lambda x: x.value/x.weight, reverse=True)
    selected_items = []
    current_weight = 0
    total_value = 0
    
    for item in items:
        if current_weight + item.weight <= capacity:
            #take the whole item
            selected_items.append((item, 1.0))  # 1.0 = 100%
            current_weight += item.weight
            total_value += item.value
        else:
            #take a fraction of the item
            remaining = capacity - current_weight
            if remaining > 0:
                fraction = remaining / item.weight
                selected_items.append((item, fraction))
                current_weight += item.weight * fraction
                total_value += item.value * fraction
            break
    
    return total_value, selected_items

def solve_knapsack():
    capacity = int(input("Enter the capacity of the knapsack: "))
    items = create_items()
    
    print("\nFractional Knapsack (Greedy):")
    frac_value, frac_items = solve_knapsack_fractional(capacity, items.copy())
    
    print("\nSelected Items (Fractional):")
    total_weight = 0
    for item, fraction in frac_items:
        if fraction == 1.0:
            print(f"Item ID: {item.item_id}, Weight: {item.weight}, Value: {item.value} (100%)")
            total_weight += item.weight
        else:
            used_weight = item.weight * fraction
            used_value = item.value * fraction
            print(f"Item ID: {item.item_id}, Weight: {used_weight:.1f}, Value: {used_value:.1f} ({fraction*100:.1f}%)")
            total_weight += used_weight
    print(f"\nTotal Value (Fractional): {frac_value:.1f}")
    print(f"Total Weight (Fractional): {total_weight:.1f}")

    print("\n Zero/One (0/1) Approach:")
    optimal_value, optimal_items = solve_knapsack_zero_one(capacity, items)
    
    print("\nSelected Items (0/1):")
    total_weight = 0
    for item in optimal_items:
        print(f"Item ID: {item.item_id}, Weight: {item.weight}, Value: {item.value}")
        total_weight += item.weight
    print(f"\nTotal Value (0/1): {optimal_value}")
    print(f"Total Weight (0/1): {total_weight}")

if __name__ == "__main__":
    solve_knapsack()

