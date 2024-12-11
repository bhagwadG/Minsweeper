import random

class Minesweeper:
    def __init__(self, rows, cols, mines):
        """
        Initializes the Minesweeper grid with the given dimensions and number of mines.
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.placeMines()

    def placeMines(self):
        """
        Places mines randomly on the grid using random.choice while ensuring no duplicates.
        """
        indices = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        seen_indices = set()
        i = 0
        while i < self.mines:
            rand_index = random.choice(indices)
            if rand_index not in seen_indices:
                seen_indices.add(rand_index)
                self.grid[rand_index[0]][rand_index[1]] = -1
                i += 1

    def calculateAdjacent(self, r, c):
        """
        Calculates the number of adjacent mines for a given cell (8 in total for each cell centered at 0,0)
        """
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == -1:
                count += 1
        return count

    def click(self, row, col):
        """
        Handles a user click on the specified cell. If the cell contains a mine, the game ends.
        Otherwise, it reveals cells recursively.
        """
        if self.grid[row][col] == -1:
            return "Mine hit, game over!"
        
        self.revealCells(row, col) # reveal the cells if not hit a mine
        return self.displayGrid() # display current state of board

    def revealCells(self, row, col):
        """
        Reveals the cell at (row, col) and recursively reveals adjacent cells using a stack.
        Basically DFS till we explore all the cells in case 0 is encountered
        """
        stack = [(row, col)]
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        while stack:
            r, c = stack.pop()
            if not (0 <= r < self.rows and 0 <= c < self.cols) or self.revealed[r][c]:
                continue

            self.revealed[r][c] = True
            self.grid[r][c] = self.calculateAdjacent(r, c)

            if self.grid[r][c] == 0:
                for dr, dc in directions:
                    stack.append((r + dr, c + dc))

    def displayGrid(self):
        """
        Returns a string representation of the grid showing revealed and unrevealed cells.
        """
        return "\n".join(
            " ".join("*" if self.revealed[r][c] and self.grid[r][c] == -1 else
                      str(self.grid[r][c]) if self.revealed[r][c] else "#"
                      for c in range(self.cols))
            for r in range(self.rows)
        )

# Example Usage
if __name__ == "__main__":
    game = Minesweeper(5, 5, 5)
    print("Initial Grid:")
    print(game.displayGrid())
    print("\nClicking on cell (1, 1):")
    print(game.click(1, 1))
    print("\nClicking on cell (0, 0):")
    print(game.click(0, 0))

