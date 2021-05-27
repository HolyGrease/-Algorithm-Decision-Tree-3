from dataset import Dataset
from tree import make_tree
from tree import Root

def main():
	tennis = Dataset.get_tennis()

	tennis.print(10)

	tennis = tennis.shuffle()

	train, test = tennis.split_by_ratio(0.5)

	tree = make_tree(train)

	tree.print("")

if __name__ == '__main__':
	main()