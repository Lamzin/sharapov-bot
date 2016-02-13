#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>


using namespace std;


fstream in("input.txt", ios::in);


int tmp, start;
vector<int> row(24);


int solve(vector<int> row, int position) {
	//WARNING!!!23 bit - 0 flower, ..., 0 bit - 23 flower
	for (int i = 0; i < 24; i++) {
		if (position & (1 << i)) {
			row[23 - i] |= (1 << 24);
		}
	}

	for (int i = 0, j; i < 24; i++) {
		for (j = i; (row[j] & (1 << i)) == 0 && j < 24; j++);
		swap(row[i], row[j]);
		for (int g = 0; g < 24; g++) {
			if (g != i && row[g] & (1 << i)) {
				row[g] ^= row[i];
			}
		}
	}

	int result = 0;
	for (int i = 0; i < 24; i++) {
		if (row[i] & (1 << 24)) { // is variable equal 1?
			result |= (1 << i);
		}
	}
	return result;
}


int main(){ 

	in >> start;
	for (int i = 0; i < 24; i++) {
		in >> tmp >> row[i];
	}

	
	int ans = solve(row, start) ^ solve(row, (1 << 24) - 1);

	fstream out("output.txt", ios::out);
	for (int i = 23; i >= 0; i--) {
		if (ans & (1 << i)) {
			out << 23 - i << " ";
		}
	}

	out.close();

	return 0;
}
