from abc import ABC, abstractmethod
import random
import sys

class Tile(ABC):
    def __init__(self, grid, x, y):
        self._grid = grid
        self._x = x
        self._y = y
        self.is_open = False
        self.is_flagged = False

    @abstractmethod
    def __str__(self):
        if self.is_flagged:
            return "F"
        if not self.is_open:
            return "#"
        raise NotImplementedError


class TileMine(Tile):
    def __str__(self):
        if self.is_open:
            return "O"
        return super().__str__()


class TileHint(Tile):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        self._hint = None
        
    @property
    def hint(self):
        if self._hint is None:
            # Compter le nombre de mines adjacents
            hint = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    x, y = self._x + dx, self._y + dy
                    if not (0 <= x < self._grid.width and 0 <= y < self._grid.height):
                        continue
                    tile = self._grid.get_tile(x, y)
                    if isinstance(tile, TileMine):
                        hint += 1
            self._hint = hint
            print(hint)
        return self._hint
            

    def __str__(self):
        if self.is_open:
            if self.hint == 0:
                return " "
            return str(self.hint)
        return super().__str__()


class Grid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self._tiles = [[TileHint(self, x, y) for y in range(width)] 
                       for x in range(height)]
        mines_coord = self._mines_coords()
        for x, y in mines_coord:
            self._tiles[x][y]=TileMine(self, x, y)
        self.remaining = width * height - len(self._mines_coords())

    #Permet de calculer les cases avec les bombes
    def _mines_coords(self):
        all_coords = [(x, y) for x in range(self.height) for y in range(self.width)]
        num_mines = int(len(all_coords) * 0.1)
        mines_coord = random.sample(all_coords, num_mines)
        return mines_coord

    def get_tile(self, x, y):
        return self._tiles[x][y]
    
    def __str__(self):
        grid_str= ""
        for row in self._tiles:
            row_str=" ".join([str(tile) for tile in row])
            grid_str += row_str+"\n"
        return grid_str
    
    def open(self, x, y):
        tile = self.get_tile(x,y)
        if tile.is_open :
            raise Exception("Case déjà ouverte")
        elif tile.is_flagged:
            raise Exception("Case déjà flaggée")
        else:
            tile.is_open = True
            #print(self.remaining)
            self.remaining -= 1
    
    def toggle_flag(self, x, y):
        tile = self.get_tile(x,y)
        if tile.is_open:
            raise Exception("Case déjà ouverte")
        tile.is_flagged = not tile.is_flagged

           
class MineSweeper:
    def __init__(self):
        self.is_playing = False
        self.grid = None

    def open(self, x, y):
        print(x , y)
        if not self.is_playing:
            raise Exception("Aucune partie en cours")
        elif x < 0 or y < 0 or x >= self.grid.width or y >= self.grid.height:
            raise Exception("Désolé vos coordonnées sont incorrectes") 
        else:
            print(f"Ouvrir la case {x}, {y}")
            self.grid.open(x, y)
            print(self.grid)

    def flag(self, x, y):
        if not self.is_playing:
            raise Exception("Aucune partie en cours")
        elif x < 0 or y < 0 or x >= self.grid.width or y >= self.grid.height:
            raise Exception("Désolé vos coordonnées sont incorrectes") 
        else:
            print(f"Flagger la case {x}, {y}")
            self.grid.toggle_flag(x, y)
            print(self.grid)

    def new_game(self, largeur, hauteur):
        self.width = largeur
        self.height = hauteur
        self.is_playing = True
        self.grid = Grid(largeur, hauteur)
        grid = self.grid
        print(grid)   
    
    def is_win(self):
        return self.grid.remaining == 0
    
    def is_lost(self):
        return self.is_lost
    
   
        
def main():

    largeur = int(sys.argv[1])
    hauteur = int(sys.argv[2])

    game = MineSweeper()
    game.new_game(largeur, hauteur)
    

    while game.is_playing:
        inp = input("Entrez les coordonnées de la case à ouvrir ou une commande (ex: F 1 3 ou 1 2 ou newgame ou quit) : ")
        
        if inp == "quit" :
            print("vous avez quitté la partie !")
            break
        
        elif inp == "newgame" or inp == "new game":
            l = int(input("Entrer la largeur de la grille : "))
            h = int(input("Entrez la hauteur de la grille : "))
            game.new_game(l,h)
            continue
        
        tab_coor = inp.split(" ")
        
        if len(tab_coor) == 3 and tab_coor[0] == "F":
            row = int(tab_coor[1])
            col = int(tab_coor[2])
            try:
                game.flag(row, col)
            except Exception as e:
                print(e)
        
        elif len(tab_coor) == 2:
            row = int(tab_coor[0])
            col = int(tab_coor[1])
            #print(row, col)
            try:
                game.open(row, col)
            except Exception as e:
                print(e)
                
main()