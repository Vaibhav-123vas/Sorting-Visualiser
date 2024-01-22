import tkinter as tk
import random
import time

class SortingVisualizer:
    def __init__(self, master, size):
        self.master = master
        self.size = size
        self.array = [i + 1 for i in range(self.size)]
        random.shuffle(self.array)
        self.sorted = False

        # GUI Setup
        self.master.title("Sorting Visualizer")
        self.master.geometry("800x600")
        self.master.configure(bg="black")
        
        self.label = tk.Label(self.master, text="Press R for Reset | Space for Start Sorting | A for Ascending | D for Descending| I : Insertion Sort | S : Selection Sort | B : Bubble Sort | M : Merge Sort | Q : QuickSort")
        self.label.pack()

        # Heading
        self.heading_label = tk.Label(self.master, text="Sorting Visualizer", font=("Helvetica", 20), fg="white", bg="black")
        self.heading_label.pack(pady=10)

        # Size of Array
        self.size_label = tk.Label(self.master, text=f"Size of Array: {self.size}", font=("Helvetica", 12), fg="white", bg="black")
        self.size_label.pack()

        # Initial Array
        self.array_label = tk.Label(self.master, text=f"Initial Array: {self.array}", font=("Helvetica", 12), fg="white", bg="black")
        self.array_label.pack()

        # Sorted Array
        self.sorted_array_label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="white", bg="black")
        self.sorted_array_label.pack()

        # Canvas for Visualization
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="black")
        self.canvas.pack()

        # Draw the initial array
        self.draw_array()

        # Key bindings
        self.master.bind("<space>", self.start_sorting)
        self.master.bind("<A>", self.sort_ascending)
        self.master.bind("<D>", self.sort_descending)
        self.master.bind("<I>", lambda event, algorithm="insertion_sort": self.select_algorithm(event, algorithm))
        self.master.bind("<B>", lambda event, algorithm="bubble_sort": self.select_algorithm(event, algorithm))
        self.master.bind("<Q>", lambda event, algorithm="quick_sort": self.select_algorithm(event, algorithm))
        self.master.bind("<M>", lambda event, algorithm="merge_sort": self.select_algorithm(event, algorithm))
        self.master.bind("<S>", lambda event, algorithm="selection_sort": self.select_algorithm(event, algorithm))
        self.master.bind("<R>", self.reset)

    def draw_array(self):
        self.canvas.delete("all")
        bar_width = 800 / self.size
        min_val, max_val = min(self.array), max(self.array)

        for i, height in enumerate(self.array):
            x1 = i * bar_width
            y1 = 400 - height * 2
            x2 = (i + 1) * bar_width
            y2 = 400
            color = self.calculate_color(min_val, max_val, height)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        self.master.update_idletasks()

    def calculate_color(self, min_val, max_val, current_val):
        normalized_val = (current_val - min_val) / (max_val - min_val)
        red = int(255 * normalized_val)
        green = int(255 * (1 - normalized_val))
        blue = 0
        return f"#{red:02X}{green:02X}{blue:02X}"

    def start_sorting(self, event):
        if not self.sorted:
            self.sorted = True
            self.sort_algorithm()

    def sort_ascending(self, event):
        if not self.sorted:
            self.array.sort()
            self.update_array_labels()
            self.draw_array()

    def sort_descending(self, event):
        if not self.sorted:
            self.array.sort(reverse=True)
            self.update_array_labels()
            self.draw_array()

    def select_algorithm(self, event, algorithm):
        if not self.sorted:
            self.sort_algorithm = getattr(self, algorithm)
            self.sorted = True
            self.sort_algorithm()

    def reset(self, event):
        self.array = [i + 1 for i in range(self.size)]
        random.shuffle(self.array)
        self.sorted = False
        self.update_array_labels()
        self.draw_array()

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
                self.draw_array()
                time.sleep(0.01)
            self.array[j + 1] = key
            self.draw_array()
        self.update_sorted_array_label()

    def bubble_sort(self):
        n = len(self.array)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_array()
                    time.sleep(0.01)
            self.draw_array()
        self.update_sorted_array_label()

    def selection_sort(self):
        for i in range(len(self.array)):
            min_idx = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.draw_array()
            time.sleep(0.01)
        self.draw_array()
        self.update_sorted_array_label()

    def merge_sort(self, array=None):
        if array is None:
            array = self.array
        if len(array) > 1:
            mid = len(array) // 2
            left_half = array[:mid]
            right_half = array[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    array[k] = left_half[i]
                    i += 1
                else:
                    array[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                array[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                array[k] = right_half[j]
                j += 1
                k += 1

            self.draw_array()
            time.sleep(0.01)
        self.draw_array()
        self.update_sorted_array_label()

    def quick_sort(self, low=None, high=None):
        if low is None and high is None:
            low, high = 0, len(self.array) - 1
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.draw_array()
        time.sleep(0.01)
        return i + 1

    def update_array_labels(self):
        self.size_label.config(text=f"Size of Array: {self.size}")
        self.array_label.config(text=f"Initial Array: {self.array}")

    def update_sorted_array_label(self):
        self.sorted_array_label.config(text=f"Sorted Array: {self.array}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sorting Visualizer")
    root.configure(bg="black")

    size = 50  # Adjust the size of the array
    visualizer = SortingVisualizer(root, size)

    root.mainloop()
