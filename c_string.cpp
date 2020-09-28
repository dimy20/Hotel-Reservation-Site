#include <conio.h>
#include <stdio.h>
#include <fstream>

void read(char *buff, int maxSize)
{
    const char *const pEND = buff + maxSize;
    // 13 -> return key
    for (char c = _getch(); c != 13 && (buff + 1 < pEND); c = _getch(), buff++)
    {
        _putch(c);
        *buff = c;
    };
    *buff = 0;
}
void print(const char *s)
{
    for (; *s != 0; s++)
    {
        _putch(*s);
    }
}
int str2int(char *s)
{
    //loop and find start point;
    const char *ptr = s;
    for (; *ptr >= '0' && *ptr <= '9'; ptr++)
    {
    };
    ptr--;
    int res = 0;
    int factor_of_ten = 1;
    for (; ptr >= s; ptr--)
    {
        res = (*ptr - '0') * factor_of_ten;
        factor_of_ten = factor_of_ten * 10;
    }
    return res;
}
int fib(int n)
{
    if (n == 0)
        return 0;
    int res[n + 1];
    res[0] = 0;
    res[1] = 1;
    for (int i = 2; i <= n; i++)
    {
        res[i] = res[i - 1] + res[i - 2];
    }
    return res[n + 1];
}
int main(int argc, char **argv)
{
    while (!_kbhit())
        ;
    return 0;
}
