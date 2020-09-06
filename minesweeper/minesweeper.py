import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # raise NotImplementedError
        if len (self.cells) == self.count :
            return self.cells
        return set ()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # raise NotImplementedError
        if self.count == 0:
            return self.cells
        return set ()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # raise NotImplementedError
        if cell in self.cells :
            self.cells.remove (cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # raise NotImplementedError
        if cell in self.cells :
            self.cells.remove (cell)

    def get_inference (self, other) :
        """
        Returns the inference which can be obtained from the second sentence
        given that we already know the first sentence
        """
        if other.cells.issubset (self.cells) :
            return Sentence (self.cells - other.cells, self.count - other.count)
        return None


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # raise NotImplementedError

        def get_nearby_cells (cell) :
            """
            Returns the neighboring cells of the current cell.
            """
            neighbors = set ()
            for i in range (cell [0]-1,cell [0]+2) :
                for j in range (cell [1] - 1, cell [1]+2) :
                    if (i,j) == cell or i < 0 or j < 0 or i == self.height or j == self.width:
                        continue
                    neighbors.add ((i,j))
            return neighbors

        # New sentence generation due to the new information of the cell
        neighbors = get_nearby_cells (cell)
        new_sentence = Sentence (neighbors,count)
        for neigh in neighbors :
            if neigh in self.mines :
                new_sentence.mark_mine (neigh)
        new_sentence.cells -= self.safes
        new_sentence.cells -= self.moves_made

        self.knowledge.append (new_sentence)

        # The cell is added in the Moves made
        self.moves_made.add (cell)
        # The cell is added as a Safe cell 
        self.mark_safe (cell)

        def update_safes_and_mines () :
            """
            Adds new safes and mines, which can be predicted directly from
            the sentences in the knoledge base. 
            """
            update = False
            while True :
                new_safes = set ()
                new_mines = set ()
                for sentence in self.knowledge :
                    # add update the new safes if can be predicted from the sentence
                    new_safes = new_safes.union (sentence.known_safes ())
                    # add update the new mines if can be predicted from the sentence
                    new_mines = new_mines.union (sentence.known_mines ())
                # add them to safes and mines
                for safe in new_safes :
                    self.mark_safe (safe)
                for mine in new_mines :
                    self.mark_mine (mine)
                # removing the sentences which cannot provide any more knowledge
                self.knowledge = [x for x in self.knowledge if len (x.cells) > 0]
                if len (new_safes) == 0 and len (new_mines) == 0 :
                    return update
                update = True
            return None

        def generate_inferences () :
            """
            Generate and add new inferences in the existing knowledge.
            Inferences are made by using two existing sentences in the knowledge base.
            """
            generated = False
            new_inferences = []
            while True :
                for sentence1 in self.knowledge :
                    for sentence2 in self.knowledge :
                        # same sentence, do ignore
                        if sentence1 == sentence2 :
                            continue
                        # given sentence 1, can sentence 2 help infer anything 
                        inference = sentence1.get_inference (sentence2)
                        if inference is None :
                            continue
                        if inference in new_inferences or inference in self.knowledge:
                            continue
                        # updates knowledge if helpful and not duplicate 
                        new_inferences.append (inference)
                # add new knowledge to the knowledge base 
                for inference in new_inferences :
                    self.knowledge.append(inference)
                # if there are no new updates in the knowledge then exit
                if len (new_inferences) == 0 :
                    return generated
                generated = True
                new_inferences = []
            return None

        tocontinue = True
        while tocontinue :
            # add new safes and mines due to change in knowledge
            okay1 = update_safes_and_mines ()
            # add new inferences with due to change in knowledge
            okay2 = generate_inferences ()
            tocontinue = okay1 | okay2

        # remove duplicates that are present in the knowledge base
        new_inferences = []
        for sentence in self.knowledge :
            if sentence not in new_inferences :
                new_inferences.append (sentence)
        self.knowledge = new_inferences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # raise NotImplementedError
        safe_moves = self.safes.copy() - self.moves_made
        if len(safe_moves) == 0:
            return None
        return safe_moves.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # raise NotImplementedError
        
        if len(self.moves_made) + len (self.mines) == self.height * self.width :
            return None

        def get_random_cell () :
            return (random.randint (0,self.height-1),random.randint (0,self.width-1))

        cell = get_random_cell ()
        while cell in self.moves_made or cell in self.mines :
            cell = get_random_cell ()
        return cell
