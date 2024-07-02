import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import deque

# Memory Management Algorithms
def first_fit(memory_blocks, process_size):
    for i in range(len(memory_blocks)):
        if memory_blocks[i] >= process_size:
            memory_blocks[i] -= process_size
            return i
    return -1

def best_fit(memory_blocks, process_size):
    best_index = -1
    min_diff = float('inf')
    for i in range(len(memory_blocks)):
        if memory_blocks[i] >= process_size and (memory_blocks[i] - process_size) < min_diff:
            min_diff = memory_blocks[i] - process_size
            best_index = i
    if best_index != -1:
        memory_blocks[best_index] -= process_size
    return best_index

def worst_fit(memory_blocks, process_size):
    worst_index = -1
    max_diff = -1
    for i in range(len(memory_blocks)):
        if memory_blocks[i] >= process_size and (memory_blocks[i] - process_size) > max_diff:
            max_diff = memory_blocks[i] - process_size
            worst_index = i
    if worst_index != -1:
        memory_blocks[worst_index] -= process_size
    return worst_index

def next_fit(memory_blocks, process_size, last_position):
    start = last_position
    n = len(memory_blocks)
    while True:
        if memory_blocks[last_position] >= process_size:
            memory_blocks[last_position] -= process_size
            return last_position
        last_position = (last_position + 1) % n
        if last_position == start:
            return -1

# Paging Algorithms
def fifo_page_replacement(pages, frame_count):
    frame = deque()
    page_faults = 0
    for page in pages:
        if page not in frame:
            if len(frame) >= frame_count:
                frame.popleft()
            frame.append(page)
            page_faults += 1
    return page_faults

def lru_page_replacement(pages, frame_count):
    frame = []
    page_faults = 0
    for page in pages:
        if page not in frame:
            if len(frame) >= frame_count:
                frame.pop(0)
            frame.append(page)
            page_faults += 1
        else:
            frame.remove(page)
            frame.append(page)
    return page_faults

def optimal_page_replacement(pages, frame_count):
    frame = []
    page_faults = 0
    for i in range(len(pages)):
        if pages[i] not in frame:
            if len(frame) < frame_count:
                frame.append(pages[i])
            else:
                furthest_use = 0
                index = -1
                for j in range(len(frame)):
                    if frame[j] not in pages[i + 1:]:
                        index = j
                        break
                    elif pages[i + 1:].index(frame[j]) > furthest_use:
                        furthest_use = pages[i + 1:].index(frame[j])
                        index = j
                frame[index] = pages[i]
            page_faults += 1
    return page_faults

def memory_compaction(memory_blocks):
    free_memory = 0
    compacted_memory = []
    for block in memory_blocks:
        if block > 0:
            compacted_memory.append(block)
        else:
            free_memory += abs(block)
    compacted_memory.append(-free_memory)
    return compacted_memory

def visualize_memory(memory_blocks, title):
    plt.bar(range(len(memory_blocks)), memory_blocks, color='blue')
    plt.xlabel('Memory Blocks')
    plt.ylabel('Block Size')
    plt.title(title)
    plt.show()

def visualize_page_replacement(pages, frame_count, algorithm):
    if algorithm == 'FIFO':
        faults = fifo_page_replacement(pages, frame_count)
    elif algorithm == 'LRU':
        faults = lru_page_replacement(pages, frame_count)
    elif algorithm == 'Optimal':
        faults = optimal_page_replacement(pages, frame_count)
    messagebox.showinfo("Page Faults", f"Total Page Faults: {faults}")

# GUI Setup
root = tk.Tk()
root.title("Memory Management Simulation")

# Memory Allocation Inputs
tk.Label(root, text="Memory Blocks (comma separated):").grid(row=0, column=0)
memory_blocks_entry = tk.Entry(root)
memory_blocks_entry.grid(row=0, column=1)

tk.Label(root, text="Process Size:").grid(row=1, column=0)
process_size_entry = tk.Entry(root)
process_size_entry.grid(row=1, column=1)

tk.Label(root, text="Last Position (for Next-Fit):").grid(row=2, column=0)
last_position_entry = tk.Entry(root)
last_position_entry.grid(row=2, column=1)

# Paging Inputs
tk.Label(root, text="Pages (comma separated):").grid(row=3, column=0)
pages_entry = tk.Entry(root)
pages_entry.grid(row=3, column=1)

tk.Label(root, text="Frame Count:").grid(row=4, column=0)
frame_count_entry = tk.Entry(root)
frame_count_entry.grid(row=4, column=1)

def allocate_memory(algorithm):
    memory_blocks = list(map(int, memory_blocks_entry.get().split(',')))
    process_size = int(process_size_entry.get())
    if algorithm == 'First-Fit':
        index = first_fit(memory_blocks, process_size)
    elif algorithm == 'Best-Fit':
        index = best_fit(memory_blocks, process_size)
    elif algorithm == 'Worst-Fit':
        index = worst_fit(memory_blocks, process_size)
    elif algorithm == 'Next-Fit':
        last_position = int(last_position_entry.get())
        index = next_fit(memory_blocks, process_size, last_position)
    if index != -1:
        visualize_memory(memory_blocks, f"{algorithm} Allocation")
    else:
        messagebox.showwarning("Allocation Failed", "Process could not be allocated")

def compact_memory():
    memory_blocks = list(map(int, memory_blocks_entry.get().split(',')))
    compacted_memory = memory_compaction(memory_blocks)
    visualize_memory(compacted_memory, "Memory Compaction")

def replace_pages(algorithm):
    pages = list(map(int, pages_entry.get().split(',')))
    frame_count = int(frame_count_entry.get())
    visualize_page_replacement(pages, frame_count, algorithm)

# Memory Allocation Buttons
tk.Button(root, text="First-Fit", command=lambda: allocate_memory('First-Fit')).grid(row=5, column=0)
tk.Button(root, text="Best-Fit", command=lambda: allocate_memory('Best-Fit')).grid(row=5, column=1)
tk.Button(root, text="Worst-Fit", command=lambda: allocate_memory('Worst-Fit')).grid(row=5, column=2)
tk.Button(root, text="Next-Fit", command=lambda: allocate_memory('Next-Fit')).grid(row=5, column=3)

# Compaction Button
tk.Button(root, text="Memory Compaction", command=compact_memory).grid(row=6, column=0)

# Page Replacement Buttons
tk.Button(root, text="FIFO", command=lambda: replace_pages('FIFO')).grid(row=7, column=0)
tk.Button(root, text="LRU", command=lambda: replace_pages('LRU')).grid(row=7, column=1)
tk.Button(root, text="Optimal", command=lambda: replace_pages('Optimal')).grid(row=7, column=2)

root.mainloop()
