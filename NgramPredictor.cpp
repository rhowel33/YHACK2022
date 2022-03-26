#include <iostream>
#include <vector>
#include <list>
#include <set>
#include <map>
#include <string>
#include <sstream>
#include <fstream>

// include python.h

#include "NgramPredictor.h"

const std::string START_TOKEN = "<start>";
const std::string STOP_TOKEN = "<stop>";
const std::string MAP_EXTENSION = "_map.txt";
const std::list<char> PUNCT {',', '.', ';', ':', '!', '?'};

int NgramPredictor::stop() {
    for (auto const &item : state) {
        if (item == STOP_TOKEN) { return 1; }
    }
    return 0;
}

void NgramPredictor::fit() {
    bool punctFlag;
    std::ifstream fin(filename);
    while (fin >> temp) { // for each training word:
        nopunct = "";
        punctFlag = false;
        for (auto const &c : temp) { // check each character
            std::string punctChar = "";
            if (std::isalpha(c)) { // keep if alpha
                nopunct += c; 
            } 
            else {
                for (auto const &sym : PUNCT) {
                    if (sym == c) { // if punct
                        punctChar += c;
                        punctFlag = true;
                        break;
                    }
                }
                if (punctFlag) {
                    words.push_back(nopunct);
                    words.push_back(punctChar);
            break;
                }
            }
        }
        if (!punctFlag) {
            vocabulary.insert(nopunct);
            words.push_back(nopunct);   
        }
    }
    fin.close();
    if (verbose) {
        for (auto const &item : vocabulary) { std::cout << item << std::endl; }
        for (auto const &item : words) { std::cout << item << std::endl; }
    }
    for (int i=0; i < N; i++) { state.push_back(START_TOKEN); }
    for (auto const &next : words) {
        wordmap[state].push_back(next);
        state.push_back(next);
        state.pop_front();
    }
    wordmap[state].push_back(STOP_TOKEN);
    if (verbose) { 
        std::ofstream fout(filename + MAP_EXTENSION);
        for (auto const &item : wordmap) { 
            for (auto const &gram : item.first) {
                fout << gram;
                fout << ":" << std::endl;
                for (auto const &val : item.second) {
                    fout << val << " ";
                }
            }
            fout << std::endl << std::endl;
        } 
        fout.close();
    }
}

void NgramPredictor::predict() {
    bool noSpaceFlag;
    srand(time(NULL));
    state.clear();
    for (int i=0; i < N; i++) { state.push_back(START_TOKEN); }
    while (!stop()) {
        noSpaceFlag = false;
        if (wordmap[state].size() != 0) {
            int ind = rand() % wordmap[state].size();
            for (auto const &sym : PUNCT) {
                if (! wordmap[state][ind].empty()) {
                    if (sym == wordmap[state][ind].back()) { // if punct
                        noSpaceFlag = true;
                        break;
                    }
                }
            }
            if (!noSpaceFlag) { std::cout << " "; }
            std::cout << wordmap[state][ind];
            state.push_back(wordmap[state][ind]);
            state.pop_front();
        }
        else {
            std::cout << "Error: state beginning with "
                      << state.front() 
                      << " has no following words\n";
            break;
        }
    }
}

