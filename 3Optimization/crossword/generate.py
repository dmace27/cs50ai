import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # removes words from the domain that don't fit the length of the variable
        for var in self.domains:
            for word in self.domains[var].copy():
                if var.length != len(word):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False

        for word in self.domains[x].copy():
            match = False
            
            # checks every value in the domain of y
            for possible in self.domains[y]:
                if self.crossword.overlaps[x, y] != None:
                    i = self.crossword.overlaps[x, y][0]
                    j = self.crossword.overlaps[x, y][1]
                    
                    # if the overlapping letter of both words are the same
                    if word[i] == possible[j]:
                        match = True
            
            # if there is no possible match remove the word from the domain
            if match == False:
                self.domains[x].remove(word)
                revised = True

        return revised    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # if no arcs are passed in, all the arcs are loaded into the queue
        if arcs == None:
            arcs = []
            for key in self.crossword.overlaps:
                arcs.append(key)
        
        # while there are still arcs in the queue
        while len(arcs) > 0:
            x = arcs[0][0]
            y = arcs[0][1]
            del arcs[0]
            
            # enforcing arc consistency by checking every arc for possibilities
            if self.crossword.overlaps[x, y] != None:
                if self.revise(x, y):
                    if len(self.domains[x]) == 0:
                        return False
                    
                    # if there was revisions, new arcs need to be added to the queue
                    for z in self.crossword.neighbors(x):
                        if z != y:   
                            arcs.append((z, x))
            
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        for var in self.crossword.variables:
            if var not in assignment or assignment[var] == None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:
            
            # checking if the values are the correct length
            if var.length != len(assignment[var]):
                return False
            
            # checking if all the values are distinct
            for var2 in assignment:
                if assignment[var] == assignment[var2] and var != var2:
                    return False
            
            # checking for conflicts between neighboring variables
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment and assignment[neighbor] != None:
                    i, j = self.crossword.overlaps[var, neighbor]
                    word1 = assignment[var]
                    word2 = assignment[neighbor]
                    if word1[i] != word2[j]:
                        return False
        
        return True    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        least_constraing_values = []
        value_conflict_pairs = []
        
        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap == None:
                    continue
                
                # if there is overlap, counts the conflicts between domain choices
                i, j = overlap
                for n_value in self.domains[neighbor]:
                    if value[i] != n_value[j]:
                        count += 1

            value_conflict_pairs.append((value, count))

        # sort by number of conflicts (least constraining first)
        value_conflict_pairs.sort(key=lambda pair: pair[1])
        for val in value_conflict_pairs:
            least_constraing_values.append(val[0])

        return least_constraing_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min = 1000000
        bookmark = None
        for var in self.domains:
            
            # if there is a variable with a smaller domain, it is bookmarked
            if len(self.domains[var]) < min and var not in assignment:
                min = len(self.domains[var])
                bookmark = var
            
            # in the case of a tie, choose the variable with the highest degree
            elif len(self.domains[var]) == min and var not in assignment:
                if len(self.crossword.neighbors(bookmark)) < len(self.crossword.neighbors(var)):
                    bookmark = var

        return bookmark
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        
        # if the assignment isn't complete, find a possibility and try it out until it doesnt work
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment[var] = None
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
