#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int n = atoi(argv[1]);
    fib(n);
    return 0;
}

int fib(int n)
{
    if(n == 0){
        return 0;
    }else if(n == 1){
        return 1;
    }else{
        return fib(n - 2) + fib(n - 1);
    }
}
