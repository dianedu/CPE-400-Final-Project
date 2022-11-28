#pragma once

#include <iostream>
#include <vector>

class Node
{
public:
	Node();
	~Node();
	bool isDown() { return connection; }
private:
	vector<char> Neighbors;
	vector<int> Paths;
	bool connection;

};