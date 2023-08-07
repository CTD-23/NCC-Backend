#include<bits/stdc++.h>
using namespace std;
map<char,char>sym={
    // {'(',')'},
    {')','('}
};
bool checkss( string ss){
    stack<char>stak;
    for (int i = 0; i < ss.length(); i++)
    {

        if (!stak.empty()){
            if (stak.top() == sym[ss[i]]){
                stak.pop();
                continue;
            }
        }
        stak.push(ss[i]);
    }

    if (stak.empty()) return true;

    return false;
    
}

bool searchResult(vector<string> arr, string k){
    return count(arr.begin(), arr.end(), k);
}

void solve(vector<string>&ans,string ss,int &n,int i,int j){
 
    if(i>=n && j>=n){
        if(checkss(ss)){
            if(searchResult(ans, ss)) return;
            ans.push_back(ss);
            return;
        }return;
    }

    if (i<n)
    {
    ss.push_back('(');
        solve(ans,ss,n,i+1,j);  
    // ss.pop_back();
    }else{
    ss.push_back(')');
        solve(ans,ss,n,i,j+1);  
    }
    ss.pop_back();


    if (j<n)
    {
    ss.push_back(')');
        solve(ans,ss,n,i,j+1);  
    // ss.pop_back();
    }else{
    ss.push_back('(');
        solve(ans,ss,n,i+1,j);  
    }
    ss.pop_back();
    
}

int main()
{
    int n = 8;
    string ss = "";
    // if (checkss(ss)){
    //     cout<<"right"<<endl;
    // }else{
    //     cout<<"wrong"<<endl;
    // }return 0;


    vector<string>ans;
    solve(ans,ss,n,0,0);

    for(auto i:ans){
        cout<<i<<" ";
    }cout<<endl;


    return 0;
}