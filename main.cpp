#include <cstdlib>
#include <iostream>
#include <iterator>
#include <list>
#include <set>
#include <map>
#include <string>
#include <sstream>
#include <fstream>
#include <stdlib.h>

#include "NgramPredictor.h"

int main(int argc, char *argv[]) {

    bool verbose = false;
    if (argc == 4) { 
        verbose = true;
    }
    else if (argc != 3) {
        std::cout << "Usage: ./ngrams N filename\n";
        exit(1);
    }


    NgramPredictor *predictor = new NgramPredictor(std::strtol(argv[1], 
                                                               NULL, 
                                                               10),
                                                   std::string(argv[2]),
                                                   verbose);
    predictor->fit();
    predictor->predict();
    delete predictor;
    return 0;
}

