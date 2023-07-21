#include <bits/stdc++.h>

using namespace std;



bool check(vector<long long >arr,int s,int l){
	if(s>l){
		return true;

	}

	if(arr[s]!=arr[l]) return false;

	return check(arr,++s,--l);
}

bool checkPalindrome(long long N)
{
	vector<long long> binaryNum;
    // cout<<binaryNum.size()<<endl;
 
    // counter for binary array
    long long i = 0;
    while (N > 0) {
 
        // storing remainder in binary array
        binaryNum[i] = N % 2;
        //binaryNum.push_back(N % 2) ;
        N = N / 2;
        i++;
    }
    

	return check(binaryNum,0,binaryNum.size()-1);

}

int main()
{
    int n;cin>>n;
    bool s = checkPalindrome(n);
    cout<<s<<endl;
   
return 0;
}





/*
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.

Input: s = "MCMXCIV"
Output: 1994

*/