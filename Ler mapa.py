import heapq
import tkinter as tk
from tkinter import filedialog
import math

class PathfindingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pathfinding App")

        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()

        self.map_data = None
        self.start_pos = None
        self.goal_pos = None
        self.load_button = tk.Button(self.master, text="Carregar Mapa", command=self.load_map)
        self.load_button.pack()

        self.find_path_button = tk.Button(self.master, text="Encontrar Caminho", command=self.find_path)
        self.find_path_button.pack()

        self.destination_label = tk.Label(self.master, text="Destino (x, y):")
        self.destination_label.pack()

        self.destination_entry = tk.Entry(self.master)
        self.destination_entry.pack()

        self.select_destination_button = tk.Button(self.master, text="Selecionar Destino", command=self.select_destination)
        self.select_destination_button.pack()

        self.selected_destination = None

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        if self.map_data:
            cell_size = 30
            col_index = event.x // cell_size
            row_index = event.y // cell_size

            if 0 <= col_index < len(self.map_data[0]) and 0 <= row_index < len(self.map_data):
                self.selected_destination = (col_index, row_index)
                self.destination_entry.delete(0, tk.END)
                self.destination_entry.insert(0, f"{col_index}, {row_index}")
                self.draw_map()

    def load_map(self):
        file_path = filedialog.askopenfilename(title="Selecionar arquivo de mapa", filetypes=[("Arquivos de Texto", "*.txt")])

        if file_path:
            with open(file_path, 'r') as file:
                # Lê a largura e altura do mapa
                width, height = map(int, file.readline().strip().split())

                # Lê a posição inicial
                self.start_pos = tuple(map(int, file.readline().strip().split()))

                # Lê o mapa
                self.map_data = [list(map(int, file.readline().strip().split())) for _ in range(height)]

            self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")

        if self.map_data:
            cell_size = 30
            for row_index, row in enumerate(self.map_data):
                for col_index, value in enumerate(row):
                    x1, y1 = col_index * cell_size, row_index * cell_size
                    x2, y2 = x1 + cell_size, y1 + cell_size

                    color = "white" if value >= 0 else "black"
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

            if self.start_pos:
                x, y = self.start_pos
                self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="green")

            if self.selected_destination:
                x, y = self.selected_destination
                self.canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="red")

    def find_path(self):
        if not self.map_data or not self.start_pos or not self.selected_destination:
            return

        self.goal_pos = self.selected_destination
        path = self.astar(self.start_pos, self.goal_pos)
        self.highlight_path(path)

    def select_destination(self):
        try:
            x, y = map(int, self.destination_entry.get().split(","))
            if 0 <= x < len(self.map_data[0]) and 0 <= y < len(self.map_data):
                self.selected_destination = (x, y)
                self.draw_map()
        except ValueError:
            pass

    def astar(self, start, goal):
        def heuristic(node):
            dx = abs(node[0] - goal[0])
            dy = abs(node[1] - goal[1])
            return math.sqrt(dx**2 + dy**2) + (dx + dy)  # Penalizando movimentos diagonais

        priority_queue = [(0, start)]
        visited = set()
        cost_so_far = {start: 0}
        came_from = {}

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            if current_node == goal:
                path = [current_node]
                while current_node in came_from:
                    current_node = came_from[current_node]
                    path.insert(0, current_node)
                return path

            visited.add(current_node)

            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited:
                    new_cost = cost_so_far[current_node] + self.map_data[neighbor[1]][neighbor[0]]
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + heuristic(neighbor)
                        heapq.heappush(priority_queue, (priority, neighbor))
                        came_from[neighbor] = current_node

    def get_neighbors(self, node):
        x, y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(self.map_data[0]) and 0 <= ny < len(self.map_data)
                and self.map_data[ny][nx] >= 0]

    def highlight_path(self, path):
        if not path:
            return

        for x, y in path:
            self.canvas.create_oval(x * 30 + 5, y * 30 + 5, (x + 1) * 30 - 5, (y + 1) * 30 - 5, fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
