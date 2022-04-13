import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE
    LIGHT_GRAY = 160, 160, 160
    DARK_GRAY = 192, 192, 192

    # these gradients will be used for the bars
    GRADIENTS = [
        GREY,
        LIGHT_GRAY,
        DARK_GRAY
    ]
    
    FONT = pygame.font.SysFont("arial.ttf", 30)
    LARGE_FONT = pygame.font.SysFont("arial.ttf", 40)

    SIDE_PAD = 100 # want padding on both the left and right had side
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height)) #creates the window
        pygame.display.set_caption("Sorting Algortihm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        # width of each block take the width - pad and then divde my the amount of blocks
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) 
        self.block_height = math.floor((self.height - self.TOP_PAD)/(self.max_val - self.min_val))
        
        # self side pad
        self.start_x = self.SIDE_PAD//2 

# passing a instance of the draw infomration class
def draw(draw_info, algo_name , ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1 , draw_info.GREEN)
    # used to center in middle of screen
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A-Ascending | D - Descending", 1 , draw_info.BLACK)
    # used to center in middle of screen
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,45))

    sorting = draw_info.FONT.render("I -Insertion Sort | B- Bubble Sort", 1 , draw_info.BLACK)
    # used to center in middle of screen
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info , color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,  draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        #top left point in retangular
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val)* draw_info.block_height

        #give each element a different color because the remainder will keep changing
        color = draw_info.GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]

        #draws the rectangles
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# used to genreate the list 
def generating_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        # will include both min and max value 
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

#call this function every swap
def bubble_sort(draw_info , ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range (len(lst) - 1 -i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                #swap the values
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j :draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True # generator for controls 
    return lst

def insertion_sort(draw_info, ascending = True):
   lst =draw_info.lst

   for i in range(1, len(lst)) :
       current = lst[i]

       while True:
           ascending_sort = i > 0 and lst[i-1] > current and ascending
           descending_sort = i > 0 and lst[i-1] < current and not ascending
           
           if not ascending_sort and not descending_sort:
               break
           lst[i] = lst[i-1]
           i = i-1
           lst[i] = current
           draw_list(draw_info, {i -1:draw_info.GREEN, i: draw_info.RED},True)
           yield True
   return lst
def main():
    # pygame will need a loop to continue the display
    run = True
    # regualte how many timesuickly the game will run
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generating_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800,600,lst)
    sorting = False
    ascending = True
   
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        #fps
        clock.tick(60)

        #check if the generater is done and we keep calling it constantly untill we are done
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info , sorting_algo_name , ascending)
            #this will render the display
            pygame.display.update()

        for event in pygame.event.get():
            #for hitting the exit button in top right corner
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            #reset the list   
            if event.key == pygame.K_r:
                lst = generating_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                #if reset you sorting stops and new vals generated
                sorting = False
            #can't sort if already sorting 
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                #stores the generator object thta wil be created when we call the function
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"    
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

        
    pygame.quit()


if __name__ == "__main__":
    main()
