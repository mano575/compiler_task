#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <set>
#include <algorithm>
using namespace std;

// Function to check if a grammar is simple
bool isSimpleGrammar(const map<string, vector<string>>& grammar) {
    for (const auto& [nonTerminal, rules] : grammar) {
        set<char> startingTerminals;

        for (const string& rule : rules) {
            // Rule must not contain empty string
            if (rule.empty()) {
                return false;
            }

            // Rule must start with a terminal
            char firstSymbol = rule[0];
            if (!islower(firstSymbol)) {
                return false;
            }

            // Ensure all rules for the same non-terminal start with different terminals
            if (startingTerminals.count(firstSymbol)) {
                return false; // Conflict in starting terminal
            }
            startingTerminals.insert(firstSymbol);
        }
    }
    return true; // Grammar is simple
}

// Recursive function to parse input string using the grammar
bool parse(const string& nonTerminal, const string& input, size_t& pos,
           const map<string, vector<string>>& grammar) {
    if (pos > input.size()) return false;

    for (const string& rule : grammar.at(nonTerminal)) {
        size_t tempPos = pos;
        bool isValid = true;

        for (char symbol : rule) {
            if (isupper(symbol)) {
                // Non-terminal: Recursive parsing
                if (!parse(string(1, symbol), input, tempPos, grammar)) {
                    isValid = false;
                    break;
                }
            } else {
                // Terminal: Match the symbol
                if (tempPos < input.size() && input[tempPos] == symbol) {
                    ++tempPos;
                } else {
                    isValid = false;
                    break;
                }
            }
        }

        if (isValid) {
            pos = tempPos;
            return true;
        }
    }

    return false;
}

int main() {
    map<string, vector<string>> grammar;
    string choice;

    while (true) {
        cout << "\nRecursive Descent Parsing for Simple Grammar\n";
        cout << "1- Enter Another Grammar\n2- Enter Another String\n3- Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        if (choice == "1") {
            // Input grammar from the user
            grammar.clear();
            cout << "\nEnter rules for the grammar (Type 'end' to finish):\n";

            string nonTerminal;
            while (true) {
                cout << "Enter non-terminal (or 'end' to finish): ";
                cin >> nonTerminal;
                if (nonTerminal == "end") break;

                cout << "Enter rules for " << nonTerminal << " (separate by space, end with 'end'): ";
                vector<string> rules;
                string rule;

                while (cin >> rule && rule != "end") {
                    rules.push_back(rule);
                }

                grammar[nonTerminal] = rules;
            }

            cout << "\nGrammar:\n";
            for (const auto& [nonTerminal, rules] : grammar) {
                for (const string& rule : rules) {
                    cout << nonTerminal << " --> " << rule << ", ";
                }
            }
            cout << "\b\b \n"; // Remove trailing comma and space

            if (isSimpleGrammar(grammar)) {
                cout << "The grammar is simple.\n";
            } else {
                cout << "The grammar isn't simple. Try again.\n";
                grammar.clear();
            }

        } else if (choice == "2") {
            if (grammar.empty()) {
                cout << "No grammar entered. Please enter a grammar first.\n";
                continue;
            }

            // Input string to parse
            string input;
            cout << "\nEnter the string to be checked: ";
            cin >> input;

            cout << "The input String: [";
            for (size_t i = 0; i < input.size(); ++i) {
                cout << "'" << input[i] << "'";
                if (i != input.size() - 1) cout << ", ";
            }
            cout << "]\n";

            size_t pos = 0;
            if (parse("S", input, pos, grammar) && pos == input.size()) {
                cout << "Your input string is Accepted.\n";
            } else {
                cout << "Your input string is Rejected.\n";
            }

        } else if (choice == "3") {
            cout << "Exiting...\n";
            break;
        } else {
            cout << "Invalid choice. Try again.\n";
        }
    }

    return 0;
}
