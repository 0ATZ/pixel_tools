CC=g++

CFLAGS=-I. -I./include
ODIR=obj
INCLUDE_DIR=include
SOURCE_DIR=source


buff: $(SOURCE_DIR)/BufferIO.cpp
	$(CC) -o buff.exe $(SOURCE_DIR)/BufferIO.cpp $(CFLAGS)

test: $(SOURCE_DIR)/test.cpp
	$(CC) -o test.exe $(SOURCE_DIR)/test.cpp $(CFLAGS)

.PHONY: clean

clean:
	rm -f output/*.bin
	rm -f *.exe