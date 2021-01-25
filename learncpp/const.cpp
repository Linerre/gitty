#include <iostream>

using std::cout;
using std::cin;

int main()
{
  const int age = 16;
  int const height = 180;

  int tries = 0;
  std::cout << "Are you ready for try #" 
            << ++tries
            << "?\n";

  tries = 0;
  std::cout << "Are you ready for try #" 
            << tries++
            << "?\n";

  cout << "Height: " << height << std::endl;
  cout << "Age: " << age << std::endl;
}
