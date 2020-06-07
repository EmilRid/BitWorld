from random import randint, choice
import numpy as np
import sys
import noise

class Tile:
    pass

class Grass_Tile(Tile):
    COLOR = (11, 64, 20)
    def __str__(self):
        return "G"

class Dirt_Tile(Tile):
    COLOR = (89, 79, 29)
    def __str__(self):
        return "D"

class Water_Tile(Tile):
    COLOR = (0, 0, 128)
    def __str__(self):
        return "W"

class Sand_Tile(Tile):
    COLOR = (242, 209, 107)
    def __str__(self):
        return "S"

class Tree_Tile(Tile):
    COLOR = (5,115,60)
    soils = [Grass_Tile, Dirt_Tile]
    def canExist(self, tileUnder):
        return tileUnder in self.soils
    
    def __str__(self):
        return "T"



class Map:
    """
    The Map-object models the gamemap.
    It generates the map procedurally using snoise.

    Internally it keeps all the tiles in a dictionary.
    """
    TILE_TYPES_GROUND = [Water_Tile, Sand_Tile, Dirt_Tile, Grass_Tile]
    
    def __init__(self, initialSize = (50, 50)):
        self.grid = {}
        for x in range(initialSize[0]):
            for y in range(initialSize[1]):#-initialSize[0]//2, initialSize[0]//2-1):
                self.grid[(x,y)] = self._generateTile((x,y))

    
    def _getTile(self, position):
        if position in self.grid:
            return self.grid[position]
        else:
            tile = self._generateTile(position)
            self.grid[position] = tile
            return tile
    
    def _generateTile(self, position=None):
        

        if position != None:
            x,y = position
            height = noise.snoise2(x/100, y/100, octaves=3)

            index = int(len(self.TILE_TYPES_GROUND) * height)
            tile = self.TILE_TYPES_GROUND[index]()

            if randint(0,100) == 0 :
                tree = Tree_Tile()
                if tree.canExist(tile):
                    tile = tree

            return tile
        return choice(self.TILE_TYPES_GROUND)

    def view(self, position, viewDistance = 3):
        """
        Returns a matrix with RGB colors
        """
        minX = position[0]-viewDistance
        maxX = position[0]+viewDistance
        minY = position[1]-viewDistance
        maxY = position[1]+viewDistance
        viewMatrix = []
        for x in range(minX, maxX+1):
            lineArray = []
            for y in range(minY, maxY+1):
                tile = self._getTile((x,y))
                lineArray.append(tile.COLOR)
            viewMatrix.append(lineArray)
        return viewMatrix
        
        
    
    def __str__(self):
        minX = min(self.grid.keys(), key = lambda position: position[0])[0]
        maxX = max(self.grid.keys(), key = lambda position: position[0])[0]

        minY = min(self.grid.keys(), key = lambda position: position[1])[1]
        maxY = max(self.grid.keys(), key = lambda position: position[1])[1]
        
        mapString = []
        for x in range(minX, maxX+1):
            lineString = []
            for y in range(minY, maxY+1):
                tileChar = " "
                if (x,y) in self.grid:
                    tileChar = str(self.grid[(x,y)])
                lineString.append(tileChar)
            mapString.append(" ".join(lineString))
        return "\n".join(mapString)

    def __len__(self):
        return len(self.grid)

    def memoryUsage(self):
        return sys.getsizeof(self.grid)
    


