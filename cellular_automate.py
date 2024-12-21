import pygame
import numpy as np
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_rule_set(rule_number):
    # Convert rule number to binary and pad with zeros
    binary = format(rule_number, '08b')
    # Create dictionary for rule set
    rules = {}
    patterns = ['111', '110', '101', '100', '011', '010', '001', '000']
    for i, pattern in enumerate(patterns):
        rules[pattern] = int(binary[i])
    return rules

def apply_rule(cells, rules):
    new_cells = cells.copy()
    for i in range(1, len(cells) - 1):
        # Get the pattern of current cell and its neighbors
        pattern = ''.join(str(int(x)) for x in cells[i-1:i+2])
        # Apply rule to determine new state
        new_cells[i] = rules[pattern]
    return new_cells

def intro_window():
    rule_value = [30]  # Using list to store the value that will be modified by the callback

    def on_submit():
        try:
            rule_num = int(entry.get())
            if 0 <= rule_num <= 255:
                rule_value[0] = rule_num  # Store the valid rule number
                root.quit()
                root.destroy()
            else:
                messagebox.showerror("Error", "Please enter a number between 0 and 255")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def on_closing():
        root.quit()
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.title("Cellular Automata Introduction")
    root.geometry("750x700")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Create main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Create canvas with scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Title
    title_label = ttk.Label(scrollable_frame, text="Elementary Cellular Automata", 
                           font=("Arial", 24, "bold"))
    title_label.pack(pady=10)

    # Description
    desc_text = """Cellular automata are mathematical models that consist of a grid of cells,
where each cell's state is determined by its neighbors according to simple rules."""
    desc_label = ttk.Label(scrollable_frame, text=desc_text, font=("Arial", 15), 
                          wraplength=900)
    desc_label.pack(pady=10)

    # Rules
    rules_label = ttk.Label(scrollable_frame, text="Interesting Rules to Try:", 
                           font=("Arial", 14, "bold"))
    rules_label.pack(pady=10)

    rules_text = """
Rule 30 - Creates chaotic, random-looking patterns
Rule 90 - Creates Sierpinski triangles
Rule 110 - Creates complex patterns (Turing complete!)
Rule 184 - Creates patterns that look like traffic flow
Rule 45 - Generates serpentine patterns
Rule 54 - Creates intricate braided patterns
Rule 60 - Produces triangular fractals
Rule 73 - Forms asymmetric branching structures
Rule 150 - Creates symmetric checkerboard patterns
Rule 22 - Generates spiral-like patterns
Rule 26 - Creates delicate lace-like structures
Rule 75 - Produces symmetrical wave-like patterns
Rule 126 - Forms intricate snowflake-like designs
Rule 165 - Creates symmetric dendrite patterns
Rule 169 - Generates complex, fractal-like symmetrical structures
Rule 57 - Produces intricate meandering patterns
Rule 99 - Creates asymmetric, organic-looking formations
Rule 105 - Generates delicate, feather-like structures
Rule 129 - Forms complex, branching geometric patterns
Rule 137 - Creates patterns reminiscent of crystal growth
Rule 193 - Produces intricate, maze-like configurations
Rule 13 - Generates unpredictable, scattered patterns
Rule 41 - Creates intricate diagonal wave patterns
Rule 50 - Produces symmetric, repetitive structures
Rule 86 - Forms complex, non-symmetric branching patterns
Rule 115 - Generates patterns that look like natural textures
Rule 161 - Creates symmetric, expanding geometric designs
Rule 203 - Produces intricate, lace-like fractals
Rule 18 - Creates symmetrical, expanding patterns
Rule 37 - Generates delicate, linear structures
Rule 81 - Produces interesting triangular and spiral formations
Rule 109 - Creates complex, asymmetric patterns
Rule 146 - Generates symmetric, honeycomb-like structures
Rule 172 - Produces intricate, wave-like patterns
Rule 28 - Creates delicate, feather-like patterns
Rule 64 - Generates symmetric, crystalline structures
Rule 97 - Produces complex, branching formations
Rule 122 - Creates intricate, lace-like designs
Rule 186 - Generates patterns reminiscent of natural growth"""

    rules_text_widget = tk.Text(scrollable_frame, height=20, width=80, font=("Arial", 12))
    rules_text_widget.insert("1.0", rules_text)
    rules_text_widget.configure(state="disabled")
    rules_text_widget.pack(pady=10)

    # Input frame
    input_frame = ttk.Frame(scrollable_frame)
    input_frame.pack(pady=20)

    input_label = ttk.Label(input_frame, text="Enter rule number (0-255):", 
                           font=("Arial", 12))
    input_label.pack(side=tk.LEFT, padx=5)

    entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
    entry.pack(side=tk.LEFT, padx=5)

    submit_button = ttk.Button(input_frame, text="Start Simulation", command=on_submit)
    submit_button.pack(side=tk.LEFT, padx=5)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind mousewheel to scroll
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    root.mainloop()
    
    return rule_value[0]  # Return the stored rule number

def draw_text(surface, text, pos, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos
    surface.blit(text_surface, text_rect)
    return text_rect.height

def main():
    # Get rule number from intro window
    rule_number = intro_window()
    
    # Initialize Pygame
    pygame.init()
    
    # Constants
    WIDTH = 1200
    HEIGHT = 800
    CELL_SIZE = 2
    
    # Calculate number of cells based on screen width
    num_cells = WIDTH // CELL_SIZE
    
    # Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Cellular Automata - Rule {rule_number}")
    
    # Initialize first generation (middle cell is 1)
    current_gen = np.zeros(num_cells)
    current_gen[num_cells//2] = 1
    
    # Get rule set
    rules = get_rule_set(rule_number)
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Current row to draw
    current_row = 0
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    screen.fill(BLACK)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw current generation
        for i, cell in enumerate(current_gen):
            if cell == 1:
                pygame.draw.rect(screen, WHITE, 
                               (i * CELL_SIZE, current_row * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE))
        
        # Generate next generation
        current_gen = apply_rule(current_gen, rules)
        
        # Move to next row
        current_row += 1
        
        # Reset if we reach the bottom
        if current_row >= HEIGHT // CELL_SIZE:
            current_row = 0
            screen.fill(BLACK)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
