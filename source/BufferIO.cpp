#include <cstdio>
#include <string>
#include <iostream>

typedef unsigned short int t_pixel;
typedef t_pixel t_tile[256U];

// returns bytes written
size_t writeBuffer(const char * const filename, const void * const buffer, size_t objectSize, size_t objectCount)
{

    if (!filename || !buffer)
    {
        printf("writeBuffer: invalid parameter, null pointer detected\n");
        return 0ULL;
    }

    if (objectSize == 0ULL || objectCount == 0ULL)
    {
        printf("successfully wrote nothing.\n");
        return 0ULL;
    }

    FILE * fp =  nullptr;
    // open the file in binary write mode
    fp = fopen(filename, "wb"); 
    if (!fp)
    {
        printf("failed to open file: %s\n", filename);
        return 0ULL;
    }

    // write buffer to the file
    size_t objectsWritten = fwrite(buffer, objectSize, objectCount, fp);
    if (objectsWritten == 0ULL)
    {
        printf("failed to write file: %s\n", filename);
    }

    fclose(fp);

    size_t bytesWritten = (objectsWritten * objectSize);
    return bytesWritten;
}

size_t readBuffer(const char * const filename, void * buffer, size_t objectSize, size_t objectCount)
{
    if (!filename || !buffer)
    {
        printf("readBuffer: invalid parameter, null pointer detected\n");
        return 0ULL;
    }

    if (objectSize == 0ULL || objectCount == 0ULL)
    {
        printf("successfully read nothing.\n");
        return 0ULL;
    }

    FILE * fp =  nullptr;
    // open the file in binary write mode
    fp = fopen(filename, "rb"); 
    if (!fp)
    {
        printf("failed to open file: %s\n", filename);
        return 0ULL;
    }

    size_t objectsRead = fread(buffer, objectSize, objectCount, fp);
    if (objectsRead == 0ULL)
    {
        printf("failed to read file: %s\n", filename);
    }

    fclose(fp);

    size_t bytesRead = (objectsRead * objectSize);
    return bytesRead;
}

// writes pixels to a binary file
size_t writeRect_RGB565(const char * const filename, const size_t width, const size_t height, t_pixel color)
{
    const size_t PIXEL_COUNT = width * height;
    t_pixel buffer[PIXEL_COUNT];

    for (int i = 0; i < PIXEL_COUNT; i++)
    {
        buffer[i] = color;
    }

    // write the whole buffer
    size_t bytes_written = writeBuffer(filename, buffer, sizeof(buffer), 1ULL);
    printf("pixels written : %llu\n", bytes_written / sizeof(t_pixel));
    printf("bytes written  : %llu\n", bytes_written);
    return bytes_written;
}


size_t readRect_RGB565(const char * const filename, size_t width, size_t height)
{
    const size_t PIXEL_COUNT = width * height;
    t_pixel buffer[PIXEL_COUNT];

    // read a full buffer from the file
    size_t bytes_read = readBuffer(filename, buffer, sizeof(buffer), 1ULL);
    printf("bytes read  : %d\n", bytes_read);
    printf("first value : 0x%04x\n", buffer[0]);
    printf("last value  : 0x%04x\n", buffer[PIXEL_COUNT-1U]);
    return bytes_read;
}


// usage of args here is not very secure, but ok for simple command line tool
int main(int argc, char **argv)
{
    if (argc != 5)
    {
        printf("ERROR: usage - buff.exe [output file] [width px] [height px] [16-bit color]\n");
        return 1;
    }

    // parse the args
    const char * const filename = argv[1];
    size_t width = atoi(argv[2]);
    size_t height = atoi(argv[3]);
    size_t color = 0xFFFFU;

    // good faith effort to support both integer and hex color format
    if (argv[4][0] == '0' && tolower(argv[4][1]) == 'x')
    {
        // color was specified as hex (ex. 0xF812)
        (void) sscanf(argv[4], "%x", &color);
    }
    else
    {
        // color was specified as a plain integer (ex. 63506)
        color = atoi(argv[4]);
    }

    // write a rectangle of RGB565 pixel data to a binary file
    // on windows, ouput will be written little endian byte order
    writeRect_RGB565(filename, width, height, color);
    
    // print newline between logging
    printf("\n");

    // read a rectangle of RGB565 pixel data from a binary file
    // on windows, input will be read little endian byte order
    readRect_RGB565(filename, width, height);
    return 0;
}