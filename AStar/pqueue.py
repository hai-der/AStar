class PQueue:
    def __init__(self):
        self.pri_to_items = {}
        self.items_to_pri = {}

    def empty(self):
        return len(self.items_to_pri) == 0

    def size(self):
        return len(self.items_to_pri)

    def enqueue(self, item, pri):
        if item in self.items_to_pri:
            raise Exception("Error in pqueue.enqueue: priority queue already contains item.")

        self.items_to_pri[item] = pri
        if pri in self.pri_to_items:
            self.pri_to_items[pri].append(item)
        else:
            self.pri_to_items[pri] = [item]

    def dequeue(self):
        # super inefficient (linear), but OK for now.

        if self.empty():
            raise Exception("Error in pqueue.dequeue: queue is empty.")

        # find lowest priority
        lowest_pri = min(self.pri_to_items.keys())

        # find an item with that priority, remove from pri_to_items
        item_to_return = self.pri_to_items[lowest_pri][0]
        del self.pri_to_items[lowest_pri][0]
        if len(self.pri_to_items[lowest_pri]) == 0:
            del self.pri_to_items[lowest_pri]

        # remove from items to pri
        del self.items_to_pri[item_to_return]

        return item_to_return

    def top_priority(self):
        if self.empty():
            raise Exception("Error in pqueue.dequeue: queue is empty.")

        lowest_pri = min(self.pri_to_items.keys())
        return lowest_pri

    def get_priority(self, item):
        if self.empty() or item not in self.items_to_pri:
            raise Exception("Error in pqueue.change_priority: item is not in queue.")

        return self.items_to_pri[item]

    def change_priority(self, item, newpri):
        if self.empty() or item not in self.items_to_pri:
            raise Exception("Error in pqueue.change_priority: item is not in queue.")

        # change items to pri
        oldpri = self.items_to_pri[item]
        del self.items_to_pri[item]
        self.items_to_pri[item] = newpri

        # change pri to items
        self.pri_to_items[oldpri].remove(item)
        if len(self.pri_to_items[oldpri]) == 0:
            del self.pri_to_items[oldpri]

        if newpri in self.pri_to_items:
            self.pri_to_items[newpri].append(item)
        else:
            self.pri_to_items[newpri] = [ item ]

    def contains(self, item):
        return self.__contains__(item)

    def __contains__(self, item):
        return item in self.items_to_pri

    def debug_print(self):
        print(self.pri_to_items, "\n", self.items_to_pri)


# Note that to use custom classes in the PQueue class, you will
# need to implement __hash__ and __eq__.  If two objects are equal
# according to __eq__, then they must have the same hash code.
# The easiest way to implement these is to have __eq__ compare
# all the fields you wish --- which may not be all of them ---
# and then have __hash__ call hash on a tuple of all those same fields.
class Point:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

class Point3:  # note this class only compares x & y for equality
    def __init__(self, x_, y_, z_):
        self.x = x_
        self.y = y_
        self.z = z_

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def __repr__(self):
        return self.__str__()


## def main():
##    q = PQueue()
##    #q.debug_print()
##    q.enqueue("hello", 3)
##    q.debug_print()
##    q.dequeue()
##    q.debug_print()
##    q.debug_print()
##    q.enqueue("rhodes", 1)
##    q.enqueue("college", 2)
##    q.enqueue("computer", 4)
##    q.enqueue("science", 3)
##    q.enqueue("is", 3)
##    q.enqueue("awesome", 2)
##    q.debug_print()
##
##    while not q.empty():
##        pri = q.top_priority()
##        s = q.dequeue()
##        print("got out", s, "pri=", pri)
##
##    q = PQueue()
##    q.debug_print()
##    q.enqueue("rhodes", 1)
##    q.enqueue("college", 2)
##    q.enqueue("computer", 4)
##    q.enqueue("science", 3)
##    q.enqueue("is", 3)
##    q.enqueue("awesome", 2)
##    q.debug_print()
##
##    q.change_priority("awesome", -9)
##    q.change_priority("rhodes", 2)
##    q.change_priority("science", -9)
##    #q.enqueue("science", 42)
##    #q.change_priority("notinhere", 4)
##    q.debug_print()
##
##    while not q.empty():
##        pri = q.top_priority()
##        s = q.dequeue()
##        print("got out", s, "pri=", pri)
##
##    q2 = PQueue()
##    q2.enqueue(Point(1, 2), 1.1)
##    q2.enqueue(Point(3, 4), 2.1)
##    print("priority is: ", q2.get_priority(Point(3, 4)))
##    q2.debug_print()
##    q2.change_priority(Point(1, 2), -2.6)
##    q2.debug_print()
##    q2.enqueue(Point(5, 6), 2.1)
##    q2.debug_print()
##    q2.change_priority(Point(5, 6), 5.6)
##    q2.change_priority(Point(3, 4), 5.6)
##    q2.debug_print()
##    print("priority is:", q2.get_priority(Point(3, 4)))
##
##    print(Point(3, 4) in q2) # true
##    print(Point(3, -4) in q2)  # false
##
##    while not q2.empty():
##        pri = q2.top_priority()
##        s = q2.dequeue()
##        print("got out", s, "pri=", pri)
##
##    q3 = PQueue();
##    q3.enqueue(Point3(1, 2, 3), 10)
##    #q3.enqueue(Point3(1, 2, 6), 12)   // error, already in queue
##    q3.debug_print()
##    q3.change_priority(Point3(1, 2, 7), 16)
##    q3.debug_print()

## main()
