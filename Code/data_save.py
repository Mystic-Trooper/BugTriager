import joblib
from pandas import DataFrame
import numpy


def save():
	f = open('OutputFiles/stemmed_input.txt',"r",  encoding="utf8")
	pairs = []
	developers = set()

	for line in f:
		pair = line.rstrip().rsplit(' , ',2)
		if len(pair) == 3:
			developers.add(pair[2])
			pairs.append((pair[1], pair[2]))

	developers_list = list(developers)
	pairs = [(text, developers_list.index(developer)) for (text, developer) in pairs]

	data = DataFrame(pairs, columns = ['text', 'class'])

	data = data.reindex(numpy.random.permutation(data.index))
	joblib.dump(data, 'OutputFiles/data.pkl', compress = 9)

	f.close()

	return developers_list
