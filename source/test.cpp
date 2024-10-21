// #include <iostream>
#include <cstdio>

using namespace std;
int main(void)
{
    unsigned char buffer[10] = {
        0x01, 0x02, 0x03, 0x04, 0x05, 0x01, 0x02, 0x03, 0x04, 0x05,
    };

    FILE *ptr;
    
    ptr = fopen("./assets/sprites/test.bin","wb");  // r for read, b for binary
    if (!ptr)
    {
        printf("Null pointer!\n");
    }
    
    size_t write_count = fwrite(buffer, sizeof(buffer), 1, ptr);
    printf("bytes written: %d\n", write_count);


    if (!fclose(ptr)) printf("ERROR CLOSING FILE\n");

    unsigned char rbuffer[10] = {0};
    ptr = fopen("./assets/sprites/test.bin","rb"); 
    size_t read_count = fread(rbuffer,sizeof(rbuffer),1,ptr); // read 10 bytes to our buffer
    printf("bytes read: %d\n", read_count);

    for (int i = 0; i < 10; i++)
    {
        printf("rbuffer[%d] = %d\n", i, rbuffer[i]);
    }

    if (!fclose(ptr)) printf("ERROR CLOSING FILE\n");
    // cout << "hello world!" << endl;
    return 0;
}