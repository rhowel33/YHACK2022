#include <iostream>
#include <vector>
#include <list>
#include <set>
#include <map>
#include <string>
#include <sstream>

class NgramPredictor {
    private:
        bool verbose;
        int N;
        std::string filename;
        std::list<std::string> words;
        std::set<std::string> vocabulary;
        std::map<std::list<std::string>, std::vector<std::string>> wordmap;
        std::string temp;
        std::string nopunct;
        std::list<std::string> state;

        /*
         * Returns 0 if stop token is 
         * not contained in state; 
         * 1 if it is.
         */
        int stop();

    public:
        NgramPredictor(int n, std::string f, bool v) : filename(f), 
                                                       N(n), 
                                                       verbose(v) {} 
        /*
         * Fits the predictor using
         * the text file it was
         * initialized with.
         */
        void fit();
        
        /* 
         * Generates text using ngrams
         * from fit(). Must be run
         * after fit().
         */
        void predict();
};
