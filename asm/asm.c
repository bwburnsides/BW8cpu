#include <stdio.h>
#include <stdlib.h>

#include "include/returncodes.h"
#include "include/fileutils.h"
#include "include/list.h"

#define PROG_NAME 0
#define FILE_NAME 1
#define MAX_LINE_LENGTH 80

int main(int argc, char *argv[])
{
    // Variable declarations
    char *prog;
    char *source;
    FILE *fp;
    int c;
    char buffer[MAX_LINE_LENGTH];
    int i;

    // Ensure source file name was provided
    prog = argv[PROG_NAME];
    if (argv[FILE_NAME] == NULL)
    {
        printf("%s: usage is %s <filename>\n", prog, prog);
        exit(NO_FILENAME_SUPPLIED);
    }

    // Open source file for reading
    source = argv[FILE_NAME];
    fp = fopen(source, READ);

    // Check for successful file open
    if (fp == NULL)
    {
        printf("%s: could not open file %s\n", prog, source);
        exit(BAD_FILE_OPEN);
    }

    // Read input file to stdout
    i = 0;
    LinkedList *list = NewList();
    while ((c = getc(fp)) != EOF)
    {
        if (i == MAX_LINE_LENGTH)
        {
            append(list, buffer);
            i = 0;
        }

        if (c == ' ' || c == '\n')
        {
            buffer[i++] = '\0';
            append(list, buffer);
            i = 0;
            continue;
        }

        buffer[i++] = c;
    }
    Node *node = list->first;
    for (i = 0; i < list->length; i++)
    {
        printf("%s\n", node->string);
        node = node->next;
    }

    exit(GOOD_EXIT);
}