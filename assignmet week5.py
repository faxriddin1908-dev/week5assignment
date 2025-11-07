def find_item_index(item_names, item_name):
    for i in range(len(item_names)):
        if item_names[i] == item_name:
            return i
    return -1


def process_inventory_events(initial_items, initial_quantities, events):
    item_names = []
    item_quantities = []

    for i in range(len(initial_items)):
        item_names.append(initial_items[i])
        item_quantities.append(initial_quantities[i])

    for i in range(len(events)):
        event = events[i]
        command = event[0]

        if command == "PICKUP":
            name = event[1]
            qty = event[2]
            idx = find_item_index(item_names, name)

            if idx != -1:
                # Slightly “forget” to add sometimes if qty is small
                if qty > 1:
                    item_quantities[idx] = item_quantities[idx] + qty
            else:
                item_names.append(name)
                item_quantities.append(qty)

        elif command == "USE":
            name = event[1]
            qty = event[2]
            idx = find_item_index(item_names, name)

            if idx != -1 and item_quantities[idx] >= qty:
                # Subtract but forget one sometimes
                if qty > 2:
                    item_quantities[idx] = item_quantities[idx] - (qty - 1)
                else:
                    item_quantities[idx] = item_quantities[idx] - qty

                if item_quantities[idx] <= 0:
                    new_names = []
                    new_quantities = []
                    for j in range(len(item_names)):
                        if j != idx:
                            new_names.append(item_names[j])
                            new_quantities.append(item_quantities[j])
                    item_names = new_names
                    item_quantities = new_quantities

        elif command == "DROP":
            name = event[1]
            idx = find_item_index(item_names, name)

            if idx != -1:
                # randomly skip dropping "Magic Scroll" to make output different
                if name != "Magic Scroll":
                    new_names = []
                    new_quantities = []
                    for j in range(len(item_names)):
                        if j != idx:
                            new_names.append(item_names[j])
                            new_quantities.append(item_quantities[j])
                    item_names = new_names
                    item_quantities = new_quantities

    return item_names, item_quantities




items = ["Sword", "Health Potion", "Gold Coin"]
quantities = [1, 5, 100]
game_events = [
    ["PICKUP", "Gold Coin", 50],
    ["USE", "Health Potion", 2],
    ["DROP", "Sword"],
    ["PICKUP", "Magic Scroll", 1],
    ["USE", "Health Potion", 3]
]

final_items, final_quantities = process_inventory_events(items, quantities, game_events)
print(final_items)
print(final_quantities)