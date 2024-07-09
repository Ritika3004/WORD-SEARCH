import sys
import os

class Trie:
    def __init__(self, is_end=False):
        self.children = {}
        self.is_end = is_end

    def insert(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def build(self, words):
        for word in words:
            self.insert(word)
        return self

    def delete(self, s):
        def rec(node, s, i):
            if i == len(s):
                node.is_end = False
                return len(node.children) == 0
            else:
                next_deletion = rec(node.children[s[i]], s, i+1)
                if next_deletion:
                    del node.children[s[i]]
                return next_deletion and not node.is_end and len(node.children) == 0

class Grid:
    def __init__(self, grid_file, word_file):
        self.grid_file = grid_file
        self.word_file = word_file

    def make_grid(self):
        with open(self.grid_file, 'r') as f:
            grid = [line.strip().split() for line in f.readlines()]
        
        with open(self.word_file, 'r') as f:
            word_list = [line.strip() for line in f.readlines()]

        return grid, word_list

class Solution:
    def word_search(self, grid, words):
        def check(grid, trie, i, j, i_diff, j_diff, moves):
            n, m = len(grid), len(grid[0])
            node = trie
            start_i, start_j = i, j
            substring = ''
            while 0 <= i < n and 0 <= j < m and grid[i][j] in node.children:
                substring += grid[i][j]
                node = node.children[grid[i][j]]
                if node.is_end:
                    moves.append(((start_i, start_j), (i, j)))
                    trie.delete(substring)
                i += i_diff
                j += j_diff
        moves = []
        trie = Trie().build(words)
        n, m = len(grid), len(grid[0])
        for i in range(n):
            for j in range(m):
                if grid[i][j] in trie.children:
                    for i_diff, j_diff in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        check(grid, trie, i, j, i_diff, j_diff, moves)
        return moves

if __name__ == "__main__":
    grid_file = 'grid1.txt'
    word_file = 'medium.txt'

    grid_obj = Grid(grid_file, word_file)
    grid, word_list = grid_obj.make_grid()
    solution_obj = Solution()
    moves = solution_obj.word_search(grid, word_list)
    
    for row in grid:
        print(' '.join(row))
    
    print(moves)
