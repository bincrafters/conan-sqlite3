#include <sqlite3.h>
#include <iostream>

int main()
{
    auto ver = sqlite3_libversion();
    std::cout << "SQLite3 libversion: " << ver << "\n";
    return 0;
}

