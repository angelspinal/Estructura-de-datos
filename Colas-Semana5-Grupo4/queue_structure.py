class Queue:

    def __init__(self):
        self.__items = []

    def enqueue(self, item):
        self.__items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.__items.pop(0)

    def front(self):
        if self.is_empty():
            return None
        return self.__items[0]

    def is_empty(self):
        return len(self.__items) == 0

    def size(self):
        return len(self.__items)

    def __str__(self):
        return str(self.__items)