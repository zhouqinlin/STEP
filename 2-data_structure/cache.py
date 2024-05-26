import sys
from hash_table import HashTable

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!


# A doubly linked list node class to maintain the order of the pages.
class DoublyLinkedList:
    # |self.key|: The URL of the page.
    # |self.value|: The contents of the page.
    # |self.prev|: The previous node in the linked list.
    # |self.next|: The next node in the linked list.
    def __init__(self, key=0, value=0, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


# The cache data structure to store the most recently accessed N pages.
class Cache:
    # Initialize the cache.
    # |self.size|: The size of the cache.
    # |self.page_counter|: The number of pages currently in the cache.
    # |self.cache|: A hash table to store the pages.
    # |self.head|: The head of the doubly linked list.
    # |self.tail|: The tail of the doubly linked list.
    def __init__(self, n):
        self.size = n
        self.page_counter = 0
        self.cache = HashTable()
        self.head = DoublyLinkedList()
        self.tail = DoublyLinkedList(prev=self.head)
        self.head.next = self.tail  # Initialize the head and tail to be linked


    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        if self.cache.get(url) != (None, False):  # If the page is already in the cache
            node = self.cache.get(url)[0]  # Get the node from the hash table
            node.value = contents  # Update the contents of the node
            self.moveToHead(node)  # Move the node to the head of the linked list
        else:  # If the page is not in the cache
            node = DoublyLinkedList(url, contents)  # Create a new node
            self.addNode(node)  # Add the new node to the linked list
            self.cache.put(url, node)  # Add the new node to the hash table
            self.page_counter += 1  # Increment the page counter
            if self.page_counter > self.size:  # If the cache is full
                removedNode = self.removeTail()  # Remove the least recently accessed page
                self.cache.delete(removedNode.key)  # Remove the page from the hash table
                self.page_counter -= 1  # Decrement the page counter

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        cached_pages = []
        cur = self.head.next
        while cur.next:  # Traverse the linked list
            cached_pages.append(cur.key)
            cur = cur.next
        return cached_pages
    
    # Add a new node to the head of the linked list.
    def addNode(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        
    # Remove a node from the linked list.
    def removeNode(self, node):
        node.next.prev = node.prev
        node.prev.next = node.next

    # Move a node to the head of the linked list.
    def moveToHead(self, node):
        self.removeNode(node)
        self.addNode(node)

    # Remove the least recently accessed node (the tail) from the linked list.
    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
