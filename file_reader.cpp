#include <stdio.h>
#include <fstream>
#include <iostream>
#include <conio.h>
int main()
{
    // std::cout << "hello" << std::endl;
    std::fstream fs("text.txt", std::fstream::in | std::fstream::out);

    for (char c = fs.get(); fs.good(); c = fs.get())
    {
        _putch(c);
    }
    if (fs.eof())
    {
        printf("\n");
        printf("%s", "reached end of file");
    }
    if (fs.fail())
    {
        printf("%s", "somenthing went wrong ");
    }
    fs.close();

    return 1;
}