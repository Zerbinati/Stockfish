# simulate_book_percentages.py

def calculate_percentages(entries):
    totals = [weight + learn for weight, learn in entries]
    total_sum = sum(totals)

    if total_sum == 0:
        print("⚠️ All entries are zero — can't calculate percentages.")
        return

    print("\n📊 Resulting percentages:")
    for i, (weight, learn) in enumerate(entries):
        combined = weight + learn
        percent = (combined / total_sum) * 100
        print(f"Move {i+1}: weight={weight}, learn={learn} → {percent:.2f}%")

def main():
    print("🎯 Polyglot Book Entry Simulator")
    print("Enter weight and learn values for each move.")
    print("Example: for 2 moves of weight=100, and one has learn=+500")

    entries = []
    while True:
        try:
            w = int(input("Weight (or blank to finish): ").strip() or -1)
            if w == -1:
                break
            l = int(input("Learn: ").strip())
            entries.append((w, l))
        except ValueError:
            print("❌ Invalid input. Try again.")
    
    if entries:
        calculate_percentages(entries)
    else:
        print("No data entered.")

if __name__ == "__main__":
    main()
