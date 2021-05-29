from dataset import Dataset

class Node:
	"""Node of tree abstract class"""
	# Indent using to print tree in terminal
	indent = "\t"

class Root(Node):
	"""Root is first node of the tree (head)"""
	def __init__(self, nodes, attribute_index, attribute_name):
		"""Method create Dataset item

		Args:
			nodes (list): list of child nodes
			attribute_index (int): index of column in dataset by which splitted child nodes
			attribute_name (string): name of column in dataset by which splitted child nodes
		"""
		self.nodes = nodes
		self.attribute_index = attribute_index
		self.attribute_name = attribute_name

	def print(self, prefix=""):
		"""Method print tree to terminal

		Args:
			prefix (string): indent used for this node and children nodes
		"""
		# Print Root's attribute name
		print(prefix + self.attribute_name)
		# Print child nodes
		for node in self.nodes:
			node.print(prefix + self.indent)

	def classify(self, row):
		"""Method classify instance

		Args:
			row (list): instance to classify

		Returns:
			class: prediction for this instance
			None: if can't classify
		"""
		# Get copy of the insance
		# to not modify origin one
		row = row.copy()
		# Get attribute value
		attribute_value = row.pop(self.attribute_index)
		# Search in each child node
		for node in self.nodes:
			# If attribute value same as in child node
			if node.attribute_value == attribute_value:
				# As child node to classify
				return node.classify(row)
		# If no childs with same value
		return None

class Branch(Node):
	"""Branch is a node of the tree that fork tree"""
	def __init__(self, nodes, attribute_index, attribute_name, attribute_value):
		"""Method create Dataset item

		Args:
			nodes (list): list of child nodes
			attribute_index (int): index of column in dataset by which splitted child nodes
			attribute_name (string): name of column in dataset by which splitted child nodes
			attribute_value: value of attribute that lead to this node
		"""
		self.nodes = nodes
		self.attribute_index = attribute_index
		self.attribute_name = attribute_name
		self.attribute_value = attribute_value

	def print(self, prefix):
		"""Method print tree to terminal

		Args:
			prefix (string): indent used for this node and children nodes
		"""
		print(prefix, end=" ")
		print(self.attribute_value, end=" -> ")
		print(self.attribute_name)
		for node in self.nodes:
			node.print(prefix + self.indent)

	def classify(self, row):
		"""Method classify instance

		Args:
			row (list): instance to classify

		Returns:
			class: prediction for this instance
			None: if can't classify
		"""
		# Get attribute value
		attribute_value = row.pop(self.attribute_index)
		# Search in each child node
		for node in self.nodes:
			# If attribute value same as in child node
			if node.attribute_value == attribute_value:
				# As child node to classify
				return node.classify(row)
		# If no childs with same value
		return None

class Leaf(Node):
	"""Leaf is a node of tree that ends this Branch"""
	def __init__(self, attribute_value, target_value):
		"""Method create Dataset item

		Args:
			attribute_value: value of attribute that lead to this node
			target_value: value of node
		"""
		self.attribute_value = attribute_value
		self.target_value = target_value

	def print(self, prefix):
		"""Method print tree to terminal

		Args:
			prefix (string): indent used for this node
		"""
		# Print prefix
		print(prefix, end=" ")
		# Print attribute value that lead to this node
		print(self.attribute_value, end=" -> ")
		# Print target value
		print(f"[{self.target_value}]")

	def classify(self, row):
		"""Method classify instance

		Args:
			row (list): instance to classify

		Returns:
			class: prediction for this instance
		"""
		# Return prediction
		return self.target_value

# TODO fit the tree
def make_tree(dataset):
	"""Methods create tree based on passed dataset

	Args:
		dataset (Dataset): dataset to create tree

	Returns:
		tree (Root): tree for classification
		tree (Leaf): if dataset contains only one class
	"""
	return make_tree_helper(dataset)

def make_tree_helper(dataset, attribute_value=-1):
	"""Method create tree based on passed dataset

	Args:
		dataset (Dataset): dataset to create tree
		attribyte_value: value that leads to this part of tree
			-1 if no tree before (in this case create Root)

	Returns:
		tree (Root): tree for classification
		tree (Leaf): if dataset contains only one class
	"""
	# If dataset contains only one class
	if Dataset.entropy(dataset.get_target_column()) == 0:
		# Create and return leaf
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