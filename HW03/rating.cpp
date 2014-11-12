#include <cstdio>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

static vector<int> readList(char* filename) {
	FILE* f = fopen(filename, "r");
	int n;
	vector<int> ans(0);
	fscanf(f, "%d", &n);
	for (int i = 0; i < n; ++i) {
		int c;
		fscanf(f, "%d", &c);
		ans.push_back(c);
	}
	fclose(f);
	return ans;
}

double DCG(vector<int> const &l) {
	int n = l.size();
	double ans = 0;
	for (int i = 0; i < n; ++i) {
		ans += (pow(2.0, l[i]) - 1.0) * log(2.0) / log(i + 2.0);
	}
	return ans;
}

double NDCG(vector<int> l) {
	double ans = DCG(l);
	sort(l.begin(), l.end());
	reverse(l.begin(), l.end());
//	sort(l.rbegin(), l.rend());
	ans /= DCG(l);
	return ans;
}

static double pRel(int r) {
	return (pow(2.0, r) - 1) / pow(2.0, 3);
}

double pFound(vector<int> const &l) {
	const double pBreak = 0.15;
	double ans = 0;
	// Generally, it isn't clear what pLook[1] must be equal to
	double pLook = 1;
	int n = l.size();
	for (int i = 0; i < n; ++i) {
		ans += pRel(l[i]) * pLook;
		pLook = pLook * (1 - pRel(l[i])) * (1 - pBreak);
	}
	return ans;
}

int main(int argc, char** argv) {
	if (argc > 1) {
		vector<int> l = readList(argv[1]);
		printf("DCG  = %lf\nNDCG = %lf\npFound = %lf\n", DCG(l), NDCG(l), pFound(l));
	}
	return 0;
}
