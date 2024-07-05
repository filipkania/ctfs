#include <iostream>
#include <stdio.h>
#include <vector>
#include <cstdint>

using namespace std;

const uint8_t enc_flag[37] = {
  0x6e, 0x68, 0x78, 0x08, 0xb0, 0x77, 0x45, 0x00, 0x6f, 0x89, 0x8b, 0x04, 0xbc, 0xe8, 0xc2, 0x99,
  0x3b, 0xdc, 0x0b, 0x43, 0x4f, 0x21, 0x72, 0x56, 0xc8, 0xdd, 0xe3, 0xe8, 0x46, 0xed, 0x94, 0xd7,
  0x6f, 0x05, 0x01, 0xf4, 0xbf
};

const unsigned long long keys[] = {
  4294967292, 4294967292, 4294967102, 4166767774, 923810610, 50867904, 1181955302, 83064966, 2219043326, 3037958716, 2967652352, 1861911262, 1735161212, 2233276342, 1430256410, 2917585052, 1631478334, 2260179310, 2525184062, 586921006, 3745518478, 3610405742, 2410571558, 298081606, 1953977854, 774429788, 3403274624, 2489184302, 753143358, 2592734942, 588270332, 1869837758, 1484141034, 2565793568, 3196810006, 2097899758, 3243572348
}; // generated from gen_keys.py

int main()
{
  setvbuf(stdout, NULL, _IONBF, 0);

  int offset;
  cin >> offset;

  for (int off = offset * 6; off < (offset * 6) + 6; off++) {
    uint16_t var_1a = (uint16_t)keys[off];
    int32_t var_18 = 0;
    for (int32_t i = 0; i <= 7; i = (i + 1)) {
      int32_t var_10_1 = 0;
      for (int32_t j = 0; j <= 0xba04014; j = (j + 1)) {
        var_10_1 = (((uint32_t)((var_1a >> 0xc) ^ (((var_1a >> 8) ^ (var_1a >> 0xa)) ^ (var_1a >> 0xb)))) & 1);
        var_1a = (((int16_t)(var_10_1 << 0xf)) | (var_1a >> 1));
      }
      var_18 = ((var_18 << 1) + var_10_1);
    }
    cout << (char)(enc_flag[off] ^ var_18);
  }
  cout << endl;
}