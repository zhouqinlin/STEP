import sys
import collections
import numpy as np


class Node:
    def __init__(self, id=-1, prev=None, val="") -> None:
        self.val = val
        self.id = id
        self.prev = prev


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A mapping from a page title to the page ID (integer).
        # For example, self.titles["A"] returns the ID of the page "A".
        self.ids = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = collections.defaultdict(list)

        # Read the pages file into self.titles.
        with open(pages_file, "r", encoding="utf-8") as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert id not in self.titles, id
                self.titles[id] = title
                self.ids[title] = id
                # self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.
    def find_most_linked_pages(self):
        # link_count = {}
        link_count = collections.defaultdict(int)
        # for id in self.titles.keys():
        # link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    # return: int: path_length, list[str]: path
    # use a linked list to remember the path
    # each node points to its previous node
    def find_shortest_path(self, start, goal):
        # Start and goal page IDs
        start_id, goal_id = self.ids[start], self.ids[goal]
        # Initialize start node
        start_node = Node(id=start_id)
        goal_node = Node()
        # Queue for BFS
        queque = collections.deque([start_node])
        # Set of visited nodes
        visited = set()
        visited.add(start_id)

        found = False
        while queque:
            cur_node = queque.popleft()
            # Explore each linked page
            for children in self.links[cur_node.id]:
                if children not in visited:
                    children_node = Node(id=children, prev=cur_node)
                    # If goal is found
                    if children == goal_id:
                        goal_node = children_node
                        found = True
                        break
                    # Add to queue and visited set
                    queque.append(children_node)
                    visited.add(children)
            if found:
                break

        path = []
        path_length = 0
        # If goal node was never reached
        if goal_node.id == -1:
            print("No path found!")
            return 0, []
        # Reconstruct the path from goal to start
        cur = goal_node
        while cur:
            path.append(self.titles[cur.id])
            path_length += 1
            cur = cur.prev
        # Reverse the path to go from start to goal
        path = path[::-1]
        print("path_length:", path_length, "\npath:", path)
        return path_length, path


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(
        self, damping_factor=0.85, max_iterations=1000, tol=1.0e-4
    ):
        num_pages = len(self.titles)
        page_rank = {page: 1.0 for page in self.titles}
        new_page_rank = collections.defaultdict(int)

        for iteration in range(max_iterations):
            new_page_rank = collections.defaultdict(int)
            total_rank_share = 0
            for page in page_rank:
                # もしノード page に隣接ノードがない場合、100% を全ノードに均等に分配する
                if not self.links[page]:
                    total_rank_share += page_rank[page]
                    continue
                # ノード P のページランクの 85% は隣接ノードに均等に分配する
                rank_share = damping_factor * page_rank[page] / len(self.links[page])
                for linked_page in self.links[page]:
                    new_page_rank[linked_page] += rank_share
                # 残りの 15% は全ノードに均等に分配する
                total_rank_share += (1 - damping_factor) * page_rank[page]

            total_rank_share /= num_pages
            for page in new_page_rank:
                new_page_rank[page] += total_rank_share

            # Print the sum of the page ranks to verify they sum to a constant value
            # print("Sum of PageRanks:", sum(page_rank.values()))

            diff = sum(
                abs(new_page_rank[page] - page_rank[page]) for page in self.titles
            )
            print("diff", diff)
            if diff < tol:
                break
            page_rank = new_page_rank.copy()

        # Sort pages by page rank
        sorted_pages = sorted(new_page_rank.items(), key=lambda x: x[1], reverse=True)

        # Print the top 10 most popular pages
        print("Top 10 most popular pages:")
        for page, rank in sorted_pages[:10]:
            print(self.titles[page], ", rank:", rank)
        print()


    # Do something more interesting!!
    def find_something_more_interesting(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass


if __name__ == "__main__":
    wikipedia = Wikipedia("pages_test.txt", "links_test.txt")
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("A", "E")
    # wikipedia.find_longest_titles()
    # path_length, path = wikipedia.find_shortest_path("A", "E")
    # wikipedia.find_most_popular_pages()
    # wikipedia = Wikipedia('pages_medium.txt', 'links_medium.txt')

    wikipedia = Wikipedia("pages_large.txt", "links_large.txt")
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()



"""
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
"""
