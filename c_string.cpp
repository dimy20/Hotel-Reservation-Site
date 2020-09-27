#include <conio.h>
#include <stdio.h>
void read(char *buff, int maxSize)
{
    const char *const pEND = buff + maxSize;

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
int main(int argc, char **argv)
{
    //const char msg[] = {'p', 'u', 't', 'a', 's', 0};
    char test[5];
    read(test, 5);
    print(test);
    while (!_kbhit())
        ;
    return 0;
}