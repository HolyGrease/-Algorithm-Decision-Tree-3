import random
import csv
import math

from itertools import groupby


class Dataset():
	def __init__(self, data, target_index, columns_names, name):
		"""Method create Dataset item

		Args:
			data (list): 			list of table rows
			target_index (int): 	index of column with target attribute
			columns_names (list): 	list with columns names
		"""
		# Check data
		if data is None:
			raise ValueError("Data in None!")
		self._data = data
		# Check target_index for valid index
		if target_index >= self.get_columns_number():
			raise ValueError(f"Target index out of range! Got {target_index}, columns number: {self.get_columns_number()}")
		self._target_index = target_index
		# Check is number of columns names same as columns in data
		# If not raise exception
		if len(columns_names) != self.get_columns_number():
			raise ValueError(f"Wrong columns names number! Got {len(columns_names)}, columns number: {self.get_columns_number()}")
		self._columns_names = columns_names
		self._name = name

	# TODO pathlib
	@staticmethod
	def get_iris(path=None):
		"""Method return iris dataset
			by default dataset must be available
			by path "resources\\data\\iris\\iris.data"
			link to dataset "http://archive.ics.uci.edu/ml/datasets/Iris/"

		Args:
			path (string): Path to file with data

		Returns:
			Dataset: Dataset object based on iris data set
		"""
		# If path not specify
		if path is None:
			path = "resources\\data\\iris\\iris.data"

		# Open file as csv
		csv_reader = csv.reader(open(path), delimiter=",")
		# Save data to list
		data = []
		# For each row in file
		for row in csv_reader:

			temp = []
			# Read first 4 attributes as float
			for i in range(4):
				temp.append(float(row[i]))
			# Read last attribute as string
			temp.append(row[4])
			data.append(temp)

		# Set attributes names
		names = [
			"Sepal length", "Sepal width",
			"Petal length", "Petal width",
			"Class"]
		# Create Dataset
		dataset = Dataset(data, 4, names, "Iris")
		# return Dataset
		return dataset

	@staticmethod
	def get_tennis(path=None):
		"""Method return tennis dataset
			by default dataset must be available
			by path "resources\\data\\tennis\\tennis.data"
			link to dataset "http://archive.ics.uci.edu/ml/datasets/Iris/"

		Args:
			path (string): Path to file with data

		Returns:
			Dataset: Dataset object based on tennis data set
		"""
		# If path not specify
		if path is None:
			path = "resources\\data\\tennis\\tennis.data"

		# Open file as csv
		csv_reader = csv.reader(open(path), delimiter=",")
		# Save data to list
		data = [row for row in csv_reader]

		# Set attributes names
		names = [
			"Outlook", "Temperature",
			"Humidity", "Wind",
			"PlayTennis"]
		# Create Dataset
		dataset = Dataset(data, 4, names, "Tennis")
		# return Dataset
		return dataset

	def print(self, rows_number=None):
		"""Method prints the dataset in console

		Args:
			rows_number (int): number of rows to print
		"""
		# If number of rows to print not specify
		if rows_number is None:
			# Set number of rows in dataset
			rows_number = self.get_rows_number()
		# Print dataset name
		print(f"Name = {self._name}")
		# Print name of target attributes
		print(f"Target = {self._columns_names[self._target_index]}")
		# Print column columns_names
		for name in self._columns_names:
			# Center align of text
			print("{:^15}".format(name), end=" | ")
		# Go to new line
		print()
		# Print data as table
		for i in range(min([rows_number, self.get_rows_number()])):
			for attribute in self.data[i]:
				# Center align of text
				print("{:^15}".format(attribute), end=" | ")
			# Go to new line
			print()

	@property
	def data(self):
		return [row.copy() for row in self._data]

	@property
	def target(self):
		return self._target_index

	@target.setter
	def target(self, new_index):
		if new_index < self.get_columns_number() and new_index >= 0:
			self._target_index = new_index

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, new_name):
		self._name = new_name

	def get_row(self, index):
		"""Method return row by index

		Args:
			index (int): index of row.
				Must be large than 0 and less than rows number in dataset

		Returns:
			list: row
		"""
		# Check is index valid
		if index > self.get_rows_number() or index < 0:
			return None
		# Return copy of the row
		return data[index].copy()

	def get_column(self, index):
		"""Method returns values of required column

		Args:
			index (int): index of column to get values from

		Returns:
			list: values from requested column
			None: if index is incorrect
		"""
		# Check is index valid
		if index > self.get_columns_number() or index < 0:
			return None
		# Return column
		return [row[index] for row in self._data]

	def get_target_column(self):
		"""Method returns list of values from column with target attributes

		Returns:
			list: values from target attributes
		"""
		return self.get_column(self._target_index)

	def get_rows_number(self):
		"""Method returns number of rows in dataset

		Returns:
			int: number of rows
		"""
		return len(self._data)

	def get_columns_number(self):
		"""Method returns number of columns in dataset

		Returns:
			int: number of columns
		"""
		return len(self._data[0])

	# TODO doc
	def get_name(self, column_index):
		return self._columns_names[column_index]

	# TODO doc
	def remove_column(self, column_index):
		# Check is index valid
		if column_index > self.get_columns_number() or column_index < 0 or column_index == self.target:
			return None
		# Move target column
		if column_index < self.target:
			self.target -= 1
		# Delete column name
		self._columns_names.pop(column_index)
		# In each row remove specific attribute
		for row in self._data:
			row.pop(column_index)

	# TODO doc
	def split_by_predicate(self, index, predicate):
		"""

		"""
		# Unpacking predicate
		unpacking_predicate = lambda row: predicate(row, index)
		# Group data using this predicate
		datas = groupby(sorted(self.data, key=unpacking_predicate), key=unpacking_predicate)
		# Separate grouped datas on key value and data
		splitted_data = []
		keys = []
		for key, value in datas:
			# Save keys values
			keys.append(key)
			# Convert to list
			splitted_data.append(list(value))
		# Convert data to Datasets objects
		datasets = [
			Dataset(splitted_data[i], self._target_index, self._columns_names.copy(), self._name) 
			for i in range(len(splitted_data))]
		# Return datasets and key values
		return datasets, keys

	def split_by_ratio(self, ratio):
		"""Method split dataset into training and test parts with given ratio

		Args:
			ratio (float): percentage of training part in dataset. In range [0, 1]

		Returns:
			tuple: consists of training and test Dataset
		"""
		# Calculate length of first part of dataset
		TRAIN_DATASET_LEN = round(len(self._data) * ratio)
		# Create list of values for first dataset
		first = [
			self._data[i].copy()
			for i in range(TRAIN_DATASET_LEN)]
		# Create list of values for second dataset
		second = [
			self._data[i].copy()
			for i in range(TRAIN_DATASET_LEN, self.get_rows_number())]
		# Create two datasets and return them
		return (Dataset(first, self._target_index, self._columns_names, self._name),
			Dataset(second, self._target_index, self._columns_names, self._name))

	def shuffle(self):
		"""Method shuffle rows in dataset

		Returns:
			Dataset: Dataset with shuffled rows
		"""
		# Get data
		data = self.data
		# Shuffle data
		random.shuffle(data)
		# Create new dataset on shuffled data
		return Dataset(data, self._target_index, self._columns_names, self._name)

	# TODO different variants of normalization
	# for date type and etc.
	def normalize(self, column_index):
		"""Method normalize the specific column

		Args:
			column_index (int): index of column to normalize
		"""
		# Find minimum value in column
		minimum = min(self.get_column(column_index))
		# Find maximum value in column
		maximum = max(self.get_column(column_index))
		# For each value on column
		for row in self._data:
			# Calculate new value
			row[column_index] = (row[column_index] - minimum) / (maximum - minimum)

	# TODO doc
	def threshold(self, column_index, method=None):
		"""
		"""
		threshold = None
		# Finding threshold acording to the method
		if method is None or method == "median":
			threshold = self._find_threshold_median(column_index)
		elif method == "gain":
			threshold = self._find_threshold_gain(column_index)
		# If got unknown method
		else:
			return None
		# Use treshold to change column values
		for row in self._data:
			if row[column_index] < threshold:
				row[column_index] = 0
			else:
				row[column_index] = 1
		# Return threshold value
		return threshold

	# TODO doc
	def _find_threshold_median(self, column_index):
		"""
		"""
		# Get column
		column = self.get_column(column_index)
		# Sort
		column.sort()
		# Find median index
		med = int(self.get_rows_number() / 2)
		# Return median value
		return column[med]

	# TODO doc
	def _find_threshold_gain(self, column_index):
		"""
		"""
		column = self.get_column(column_index)
		target = self.get_target_column()
		# Concat column and target column
		# Convert to list of turples
		pairs = list(zip(column, target))
		# Sort pairs
		pairs.sort()
		# Find thresholds
		thresholds = [
			# Find average
			(pairs[i - 1][0] + pairs[i][0]) / 2
			# For each element in pairs, starting from second
			for i in range(1, len(column))
			# If target value changed
			if pairs[i - 1][1] != pairs[i][1]]
		# Remove duplicates
		thresholds = list(set(thresholds))
		# Calculate gain for each threshold
		gains = [
			Dataset.gain(
				self.get_column(column_index),
				self.get_target_column(),
				lambda x, y: x < threshold)
			for threshold in thresholds]
		# Find index of max gain
		index = gains.index(max(gains))
		# Return thresholds with max gain
		return thresholds[index]

	@staticmethod
	def entropy(column):
		"""Method calculate column entropy
		
		Args:
			column (List): list of values

		Returns:
			float: entropy of column. In the range [0, 1]
			None: if column is None
		"""
		# If column is None
		if column == None:
			# Return None
			return None
		# Group column by identity
		grouped = groupby(sorted(column))
		# Count rows number
		rows_number = len(column)
		# Count number of clases
		n = len(set(column))
		# If have only one class, in this case entropy equals 0
		if n == 1:
			# Return 0
			return 0
		# Calculate entropy
		output = 0
		# For each group
		for _, value in grouped:
			# Get list of values
			v = list(value)
			# Calculate
			output -= len(v) / rows_number * math.log(len(v)/rows_number, n)
		# Return entropy
		return output

	@staticmethod
	def gain(column, target_column, predicate=None):
		"""Method calculates gain of specific column

		Args:
			index (int): index of column
			predicate (function(x, y)): function that takes two arguments,
				used to group column

		Return:
			float: gain of column
			None: if index is wrong
		"""
		# Concat column and target column
		pairs = zip(column, target_column)
		# If predicate doesn't specified
		if predicate == None:
			unpacking_predicate = lambda x: x[0]
		# Otherwise
		else:
			# Unpacking predicate
			unpacking_predicate = lambda x: predicate(*x)
		# Group by predicate
		grouped = groupby(sorted(pairs, key=unpacking_predicate), unpacking_predicate)
		# Count row number
		rows_number = len(column)
		# Count entropy of target column
		output = Dataset.entropy(target_column)
		# For each group
		for _, value in grouped:
			# Get list of values
			v = list(value)
			# Calculate
			output -= len(v) / rows_number * Dataset.entropy(v)
		# Return entropy
		return output
