from alnoms.dsa.structures import Stack, Queue, Bag, SinglyLinkedList, DoublyLinkedList


def test_stack_push_pop():
    s = Stack[int]()
    assert s.is_empty()
    s.push(1)
    s.push(2)
    assert s.size() == 2
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()


def test_queue_enqueue_dequeue():
    q = Queue[int]()
    q.enqueue(1)
    q.enqueue(2)
    assert q.size() == 2
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.is_empty()


def test_bag_add_iter():
    b = Bag[int]()
    b.add(1)
    b.add(2)
    assert b.size() == 2
    assert sorted(list(b)) == [1, 2]


def test_singly_linked_list_insert_and_remove():
    lst = SinglyLinkedList()
    lst.insert_at_head(1)
    lst.append(2)
    assert len(lst) == 2
    assert lst.remove(1)
    assert len(lst) == 1


def test_doubly_linked_list_append_prepend():
    dl = DoublyLinkedList()
    dl.append(1)
    dl.prepend(0)
    assert list(dl) == [0, 1]
    assert dl.display_forward() == "0 <-> 1"
