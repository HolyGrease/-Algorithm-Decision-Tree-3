from dataset import Dataset

class Node:
	indent = "\t"

class Root(Node):
	def __init__(self, nodes, attribute_index, attribute_name):
		self.nodes = nodes
		self.attribute_index = attribute_index
		self.attribute_name = attribute_name

	def print(self, prefix=""):
		print(prefix + self.attribute_name)
		for node in self.nodes:
			node.print(prefix + self.indent)

	def classify(self, row):
		row = row.copy()
		attribute_value = row.pop(self.attribute_index)
		for node in self.nodes:
			if node.attribute_value == attribute_value:
				return node.classify(row)

		return None

class Branch(Node):
	def __init__(self, nodes, attribute_index, attribute_name, attribute_value):
		self.nodes = nodes
		self.attribute_index = attribute_index
		self.attribute_name = attribute_name
		self.attribute_value = attribute_value

	def print(self, prefix):
		print(prefix, end=" ")
		print(self.attribute_value, end=" -> ")
		print(self.attribute_name)
		for node in self.nodes:
			node.print(prefix + self.indent)

	def classify(self, row):
		attribute_value = row.pop(self.attribute_index)
		for node in self.nodes:
			if node.attribute_value == attribute_value:
				return node.classify(row)

		return None

class Leaf(Node):
	def __init__(self, attribute_value, target_value):
		self.attribute_value = attribute_value
		self.target_value = target_value

	def print(self, prefix):
		print(prefix, end=" ")
		print(self.attribute_value, end=" -> ")
		print(f"[{self.target_value}]")

	def classify(self, row):
		return self.target_value

"""
Outlook
	Sunny -> Humidity
		High -> No
		Normal -> Yes
	Overcast -> Yes
	Wind
		Strong -> No
		Weak -> Yes
"""

def make_tree(dataset):
	return make_tree_helper(dataset)

# TODO fit the tree
def make_tree_helper(dataset, attribute_value=-1):
	# If dataset contains only one class
	if Dataset.entropy(dataset.get_target_column()) == 0:
		#
		return Leaf(attribute_value, dataset.get_target_column()[0])
	# If dataset contains only one column (target column)
	if dataset.get_columns_number() == 1:
		# Split dataset by target column value
		datasets, keys = dataset.split_by_predicate(
			dataset.target, 
			lambda row, index: row[dataset.target])
		# Count sizes of each dataset
		sizes = [value.get_columns_number() for value in datasets]
		# Convert sizes and keys to list of turples
		pairs = list(zip(sizes, keys))
		# Get key value of biggest dataset
		prediction = max(pairs)[1]
		# Create Leaf
		return Leaf(attribute_value, prediction)

	# Calculate gains for each column
	gains = [
		(
			Dataset.gain(dataset.get_column(j), dataset.get_target_column()),
			j)
		for j in range(dataset.get_columns_number())
		if j != dataset.target]
	# Get index of column with max gain
	_, index = max(gains)
	# Split dataset by column value with this index
	datasets, keys = dataset.split_by_predicate(index, lambda row, index: row[index])
	# Remove column by index
	for data_set in datasets:
		data_set.remove_column(index)
	# Recalculate index
	# For each dataset recursively creating trees
	nodes = [
		make_tree_helper(datasets[i], keys[i])
		for i in range(len(datasets))]
	# If no Root created - create Root
	if attribute_value == -1:
		return Root(nodes, index, dataset.get_name(index))
	# Otherwise create Branch
	return Branch(nodes, index, dataset.get_name(index), attribute_value)