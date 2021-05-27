# Example of creating Dataset object
Firstly, import Dataset:

	from dataset import Dataset

Secondly, get some data:

	data = [
		[5.1, 3.5, 1.4, 0.2, "Iris-setosa"],
		[5.0, 3.2, 1.2, 0.2, "Iris-setosa"],
		[6.4, 3.2, 4.5, 1.5, "Iris-versicolor"],
		[6.7, 3.1, 4.4, 1.4, "Iris-versicolor"],
		[6.7, 3.0, 5.2, 2.3, "Iris-virginica"]]

Thirdly, set columns (attributes) names:

	column_names = [
		"Sepal length", "Sepal width",
		"Petal length", "Petal width",
		"Class"]

Now we can create Dataset object. Arguments:
- data - just list of list
- target index - index of target attribute, attribute that contains classes values
- column or attributes names - list of attributes names
- name - Dataset name


	iris = Dataset(data, 4, column_names, "Iris")

Also you can just get iris dataset by calling method

	get_iris().

You can specify path to dataset file by passing this path as argument, for example:

	get_iris("data\\iris.data")

Default value of path 
> resources\\data\\iris\\iris.data.

	iris = get_iris()

# Preprocessing dataset
Threshold - process of converting continius values to discrete values. There are two methods:
- median - thresholding by median value of column
- gain - thresholding by using value with maximum gain

As first argument takes column index, second - name of method

	iris.threshold(i, "gain")

Shuffle dataset:

	iris = iris.shuffle()

Split dataset on "train" and "test", as argument passing ratio. Train dataset gets 80% of original dataset, test - other:

	train, test = iris.split_by_ration(0.8)

# Creating tree
For this purpose import tree.py

	from tree import make_tree
	from tree import Root

To create decision tree use make_tree method. This method takes one argument - dataset. Return tree object.

	tree = make_tree(train)

# Classification
For classify the instance use method classify. May return None if can't classify this instance.

	instance_to_classify = [4.8, 3.1, 1.6, 0.2]
	predicted_class = tree.classify(instance_to_classify)