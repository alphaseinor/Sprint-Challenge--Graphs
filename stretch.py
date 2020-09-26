from room import Room
from player import Player
from world import World
import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# locked up on backtrack too much so I'm taking it away
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# need to define opposite path is
reverse = {"n":"s","e":"w","s":"n","w":"e"}
# player.current_room.id store in a graph?
# player.current_room.get_exits() how many have ? in it?
traversal_graph = {player.current_room.id: {d:"?" for d in player.current_room.get_exits()}}
#player.current_room.id: {d:"?" for d in player.current_room.get_exits()}

def exits(room):
    possible_directions = []
    #for d in #need a traversal graph...
    for d in traversal_graph[room]:
        if traversal_graph[room][d] == "?":
            possible_directions.append(d)
    print(f"possible directions {possible_directions} in room {room}")
    return(possible_directions)

def traversal(room):
    # print("in traversal")

    while len(exits(room)) > 0:
        print("room", room)
        random_direction = random.choice(exits(room))
        
        # store current location as previous
        previous = player.current_room.id
        # move in random direction
        player.travel(random_direction)
        # store new location as curent
        current = player.current_room.id
        # add the direction that was taken to the path
        traversal_path.append(random_direction)

        #determine if we've visited before
        if current not in traversal_graph:
            traversal_graph[current] = {d: "?" for d in player.current_room.get_exits()}

        traversal_graph[current][reverse[random_direction]] = previous
        traversal_graph[previous][random_direction] = current
        room = current
        print(f"go {random_direction} to {room}")

    return(room)

def traversal_rec(room, path_length = 0):
    room_exits = (exits(room))

    len(room_exits) > 0:
        return path_length

    print("room", room, path_length, room_exits)  

        
        

visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# print(traversal_graph)
# print(exits(player.current_room.id))
# print(traversal_graph)
# print(traversal_path)
print(traversal_rec(player.current_room.id))
# print(traversal_graph)
print(traversal_path)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

