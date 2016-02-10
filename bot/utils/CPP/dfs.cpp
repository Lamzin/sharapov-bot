#include <fstream>
#include <iostream>
#include <vector>


using namespace std;


#define POSITION 0
#define PARENT 1
#define EDGE 2
#define FINISH 16777215
#define SIZE 16777216


fstream in("input.txt", ios::in);
fstream out("output.txt", ios::out);


vector<int> way_to_finish;
int used[SIZE];
int queue[SIZE][3];


int edge[24], tmp, queue_size = 0, start, current_position;


int main() {

	in >> start;
	for (int i = 0; i < 24; i++) {
		in >> tmp >> edge[i];
	}
	
	used[start] = 1;
	queue[queue_size][POSITION] = start;
	queue[queue_size][PARENT] = -1;
	queue[queue_size][EDGE] = -1;
	queue_size++;

	for (int i = 0; i < queue_size; i++) {
		for (int j = 0; j < 24 && i < queue_size; j++) {
			current_position = queue[i][POSITION] ^ edge[j];
			if (!used[current_position]) {
				used[current_position] = 1;
				queue[queue_size][POSITION] = current_position;
				queue[queue_size][PARENT] = i;
				queue[queue_size][EDGE] = j;
				queue_size++;
				if (current_position == FINISH) {
					i = queue_size;
				}
			}
		}

	}

	for (int i = queue_size - 1; i != -1; ) {
		if (queue[i][EDGE] != -1) {
			way_to_finish.push_back(queue[i][EDGE]);
		}
		i = queue[i][PARENT];
	}

	for (int i = way_to_finish.size() - 1; i >= 0; i--) {
		out << way_to_finish[i] << " ";
	}

	out << endl;

	return 0;
}
