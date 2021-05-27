from dataset import Dataset
from tree import make_tree
from tree import Root

def main():
	iris = Dataset.get_iris()

	for i in range(4):
		iris.threshold(i, "gain")

	iris.print(10)

	iris = iris.shuffle()

	train, test = iris.split_by_ratio(0.5)

	tree = make_tree(train)

	correct = 0
	for row in test.data:
		# Get correct value
		assert_value = row.pop(test.target)
		# Make prediction
		predicted_class = tree.classify(row)
		# If prediction is correct
		if predicted_class == assert_value:
			correct += 1
		if predicted_class is None:
			predicted_class = "None"
		# Print compare log to termainal
		print("{:<15} ?= {:<15}".format(assert_value, predicted_class))
	# Count and print accuracy
	print("Acurracy: {:1.2}".format(correct / test.get_rows_number()))

if __name__ == '__main__':
	main()