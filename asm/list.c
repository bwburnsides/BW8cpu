#include <stdlib.h>
#include <stdio.h>

#include "include/list.h"

LinkedList *NewList()
{
    LinkedList *list = (LinkedList *)malloc(sizeof(LinkedList));
    list->first = NULL;
    list->last = NULL;
    list->length = 0;
    return list;
}

int append(LinkedList *list, char *string)
{
    Node *node = NewNode(string);
    if (node == NULL)
        return 0;

    if (list->first == NULL)
    {
        list->first = node;
    }
    else
    {
        list->last->next = node;
    }

    list->last = node;
    list->length++;

    return 1;
}

Node *NewNode(char *string)
{
    Node *new_node = (Node *)malloc(sizeof(Node));
    new_node->next = NULL;
    new_node->prev = NULL;
    new_node->string = string;
    return new_node;
};