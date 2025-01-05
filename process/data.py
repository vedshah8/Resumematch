import json

with open("dataset.json", "r") as file:
    data = json.load(file)

split1 = int(0.2 * len(data))
split2 = int(0.95 * len(data))
train_data = data[:split1]
test_data = data[split2:]

with open("train.json", "w") as train_file:
    json.dump(train_data, train_file, indent=4)

with open("test.json", "w") as test_file:
    json.dump(test_data, test_file, indent=4)
