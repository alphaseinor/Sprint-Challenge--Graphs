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
# traversal_path = []

# # need to define opposite path is
# reverse = {"n":"s","e":"w","s":"n","w":"e"}
# # player.current_room.id store in a graph?
# # player.current_room.get_exits() how many have ? in it?
# traversal_graph = {player.current_room.id: {d:"?" for d in player.current_room.get_exits()}}

# def exits(room):
#     directions = []
#     #for d in #need a traversal graph...
#     for d in traversal_graph[room]:
#         if traversal_graph[room][d] == "?":
#             directions.append(d)
#     return(directions)

# def traversal(room):
#     # print("in traversal")
#     while len(exits(room)) > 0:
#         random_direction = exits(room)[len(exits(room))-1]
#         # print("exits: ", exits(player.current_room.id))
#         # store current location as previous
#         previous = player.current_room.id
#         # move in random direction
#         player.travel(random_direction)
#         # store new location as curent
#         current = player.current_room.id
#         # add the direction that was taken to the path
#         traversal_path.append(random_direction)

#         #determine if we've visited before
#         if current not in traversal_graph:
#             traversal_graph[current] = {d: "?" for d in player.current_room.get_exits()}

#         traversal_graph[current][reverse[random_direction]] = previous
#         traversal_graph[previous][random_direction] = current
#         room = current

# def search_nearest_room(room):
#     q = Queue()
#     q.enqueue(room)
#     visted = set()

#     while q.size() > 0:
#         # room number
#         node = q.dequeue()

#         if node not in visted:
#             visted.add(node)
#             if len(exits(node)) > 0:
#                 print("last junction: ", node, q.size)
#                 return node
#             for room in list(traversal_graph[node].values()):
#                 q.enqueue(room)

# def backtrack(room, nearest_room):
#     q = Queue()
#     q.enqueue([room])
#     visited = set()
#     temp_node = []

#     if nearest_room == None:
#         # print("none")
#         return temp_node

#     while q.size() > 0:
#         # print("btwhile")
#         node = q.dequeue()
#         if node[-1] not in visited:
#             # print("first if")
#             visited.add(node[-1])
#             # print("backtrack", [node[-1]], nearest_room, node)
#             if node[-1] == nearest_room:
#                 # print("first if in if")
#                 temp_node = node
#                 #  print("temp_node", temp_node)
#                 break
#         # print("prefor")
#         for d in list(traversal_graph[node[-1]].values()):
#             path = list(node) + [d]
#             print(path)
#             q.enqueue(path)

#     result = []
#     # print("found match")
#     for vertex in range(len(temp_node) - 1):
#         for current in traversal_graph[temp_node[vertex]]:
#             if traversal_graph[temp_node[vertex]][current] == temp_node[vertex+1]:
#                 result.append(current)
#     # print("result: ", result)
#     return result

# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

traversal_path = []
room_keys = {}
unvisited = {}
reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'} #use this to reverse course
directions = ['n', 'e', 's', 'w'] #possible directions

def exits():
    exits = {}
    for ex in player.current_room.get_exits():
        exits[ex] = '?'
    # print(exits)
    return exits

# def exits(room):
#     directions = []
#     #for d in #need a traversal graph...
#     for d in traversal_graph[room]:
#         if traversal_graph[room][d] == "?":
#             directions.append(d)
#     return(directions)

# This Removes rooms from unvisited
def update_unvisited():
    rooms_to_del = []
    for key in unvisited:
        del_room = True
        for direction in unvisited[key]:
            if unvisited[key][direction] == '?':
                del_room = False
        if del_room:
            rooms_to_del.append(key)
    for i in rooms_to_del:
        unvisited.pop(i)
# Function to move in a direction
def move_direction(movement, prev):
    player.travel(movement)

    # exits for room? set if not already there
    if player.current_room.id not in room_keys:
        ex = exits()
        room_keys[player.current_room.id] = ex
        unvisited[player.current_room.id] = ex
        # print(room_keys)

    room_keys[player.current_room.id][reverse[movement]] = prev
    room_keys[prev][movement] = player.current_room.id
    traversal_path.append(movement)

# Main function, invoke this with the starting room id
def move(starting_room):
    if len(unvisited) > 0:
        # Cycle through directions
        for direction in directions:
            if direction in room_keys[starting_room]:
                if room_keys[starting_room][direction] == '?':
                    print(direction, room_keys[starting_room])
                    move_direction(direction, starting_room)
                    traversal_index = len(traversal_path) - 1
                    update_unvisited()
                    move(player.current_room.id)
                    if len(unvisited) > 0:
                        backtrack(traversal_index)
        return
def backtrack(traversal_index):
    move_direction(reverse[traversal_path[traversal_index]], player.current_room.id)

# Start the move_player()
#set initial state
room_keys[player.current_room.id] = exits()
unvisited[player.current_room.id] = room_keys[player.current_room.id]
#run the traversal
move(player.current_room.id)

# while len(traversal_graph) < len(room_graph):
#     print("left: ", len(room_graph) - len(traversal_graph))
#     traversal(player.current_room.id)
#     nearest_room = search_nearest_room(player.current_room.id)
#     breadcrumb = backtrack(player.current_room.id, nearest_room)
#     # print(breadcrumb)

#     for current in breadcrumb:
#         player.travel(current)
#         traversal_path.append(current)

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

