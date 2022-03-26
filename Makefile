all: main.cpp NgramPredictor.cpp
	g++ -o ngrams main.cpp NgramPredictor.cpp
debug: main.cpp NgramPredictor.cpp
	g++ -g -o debug main.cpp NgramPredictor.cpp

