import enum
import pygame
import random
import math
from animate import animate_loading
pygame.init()


class Information():
    width = 800
    height = 800
    SIDE_PAD = 150
    TOP_PAD = 120
    BOTTOM_PAD = 100
    BOTH_PAD = TOP_PAD + BOTTOM_PAD
    background_color = (255, 255, 255)
    green = 0, 255, 0
    red = 255, 0, 0
    GRADIENTS = [  # grey
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    GRADIENTS2 = [  # light blue
        (175, 238, 238),
        (206, 246, 245),
        (238, 248, 247)
    ]
    GRADIENTS3 = [  # light green
        (139, 249, 146),
        (185, 255, 185),
        (210, 255, 213)
    ]
    GRADIENTS4 = [  # light purple
        (224, 196, 231),
        (232, 216, 237),
        (241, 237, 244)
    ]
    FONT = pygame.font.SysFont('avenir', 16)
    MED_FONT = pygame.font.SysFont('avenir', 20)
    LARGE_FONT = pygame.font.SysFont('helvetica neue', 25)

    algo_img = pygame.image.load('images/algo_color.png')
    star_img = pygame.image.load('images/star.png')

    def __init__(self, lst):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.BOTH_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2
        self.start_y = self.height - self.BOTTOM_PAD


def generate_start_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(info, algo_name, ascending):
    title = info.LARGE_FONT.render(
        f"{algo_name} - { 'Ascending' if ascending else 'Descending'}", True, (0, 0, 0,))
    info.screen.blit(title, (info.width/2 - title.get_width()/2, 15))

    controls = info.FONT.render(
        "Press R - Reset     |     Press A - Ascending     |     Press D - Descending", True, (0, 0, 0))
    info.screen.blit(controls, (info.width/2 - controls.get_width()/2, 55))

    draw_block(info)

    info.screen.blit(info.algo_img, (50, 93))

    controls2 = info.FONT.render(
        "<--- select sorting method --->", True, (0, 0, 0))
    info.screen.blit(controls2, (info.width/2 -
                     controls2.get_width()/2, info.start_y + 26))

    start = info.MED_FONT.render("Press Spacebar to start", True, (0, 0, 0))
    info.screen.blit(
        start, (info.width/2 - start.get_width()/2, info.start_y + 50))


def draw_star(info, index):
    info.screen.blit(info.star_img, (158 + (index * 142), 80))


def draw_block(info, color_change={}):
    lst = info.lst
    for i, n in enumerate(lst):
        x = info.start_x + (i * info.block_width)
        y = info.start_y - ((n - info.min_val) * info.block_height)
        color = info.GRADIENTS[i % 3]

        if i in color_change:
            color = color_change[i]

        pygame.draw.rect(info.screen, color,
                         (x, y, info.block_width, info.height))
        pygame.draw.rect(info.screen, info.background_color,
                         (0, info.start_y + 10, info.width, info.height))


def animated(info, value, sort_name, ascending=True):
    backward_animate = {0: 23, 1: 22, 2: 21, 3: 20, 4: 19, 5: 18, 6: 17, 7: 16, 8: 15, 9: 14, 10: 13,
                        11: 12, 12: 11, 13: 10, 14: 9, 15: 8, 16: 7, 17: 6, 18: 5, 19: 4, 20: 3, 21: 2, 22: 1, 23: 0}
    if not ascending and value <= 23:
        value = backward_animate[value]
    if value <= 23:
        info.screen.blit(animate_loading[value], (250, 0))
    texting = info.FONT.render(
        f"{sort_name}ing in {'ascending order' if ascending else 'Descending order'}", True, (0, 0, 0))
    info.screen.blit(
        texting, (info.width/2 - texting.get_width()/2, 120))


def bubble_sort(info, sort_name, ascending=True):
    lst = info.lst
    value = 0
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_block(
                    info, {j + 1: info.green, j: info.GRADIENTS3[2], j+2: info.GRADIENTS3[1]})
                if value == 23:
                    value = 0

                animated(info, value, sort_name, ascending)
                value += 1
                pygame.display.update()
                yield True

    return lst


def selection_sort(info, sort_name, ascending=True):
    lst = info.lst
    n = len(lst)
    value = 0
    for i in range(n):
        index1 = i
        for j in range(i+1, n):
            if (lst[index1] > lst[j] and ascending) or (lst[index1] < lst[j] and not ascending):
                index1 = j
        lst[i], lst[index1] = lst[index1], lst[i]
        draw_block(
            info, {i: info.green, index1: info.red})
        if value == 23:
            value = 0
        animated(info, value, sort_name, ascending)
        pygame.display.update()
        pygame.time.delay(50)
        value += 1
        yield True
    return lst


def insertion_sort(info, sort_name, ascending=True):
    lst = info.lst
    value = 0
    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_block(
                info, {i: info.green, i+1: info.GRADIENTS4[1], i-1: info.GRADIENTS4[0]})
            if value == 23:
                value = 0
            animated(info, value, sort_name, ascending)
            pygame.display.update()
            value += 1
            yield True
    return lst


def draw_buckets(buckets, info, process=1, color_change={}):
    for i, arr in enumerate(buckets):
        for j, n in enumerate(arr):
            x = (info.start_x) + \
                (j * (info.block_width * 0.6)) + (i * 80)
            y = ((n + 5) * (info.block_height * 0.55))

            color = info.GRADIENTS2[j % 3]
            if i in color_change and color_change[i] == j and process == 1:
                color = info.green

            if i in color_change and process == 2:
                color = color_change[i][j % 3]

            if i in color_change and color_change[i] == j-1 and process == 3:
                color = info.red

            pygame.draw.rect(info.screen, color,
                             (x, 100, info.block_width, y))
            if process == 1:
                text1 = info.MED_FONT.render(
                    "Puting each element into buckets...", True, (0, 0, 0))
            if process == 2:
                text1 = info.MED_FONT.render(
                    "Sorting each buckets...", True, (0, 0, 0))
            if process == 3:
                text1 = info.MED_FONT.render(
                    "Returning each element back...", True, (0, 0, 0))

    info.screen.blit(text1, (info.width/2 - text1.get_width()/2, 60))


def bucket_sort(info, sort_name, ascending=True):
    lst = info.lst
    n = len(lst)

    buckets_size = 11

    # create empty buckets
    buckets = [[] for i in range(9)]
    index_temp = 0
    # Assign each element into buckets
    for i in range(n):
        if math.floor(lst[i]/buckets_size) == 0:
            index = 0
        else:
            index = math.floor((lst[i]/buckets_size) - 1)
        if not ascending:
            index = (index + 2) * -1
            if index == -10:
                index = -9
        if index != n:
            buckets[index].append(lst[i])

        else:
            buckets[n - 1].append(lst[i])

        draw_buckets(buckets, info, 1, {
                     index: buckets[index].index(lst[i])})
        lst[i] = 5
        draw_block(info, {i: info.red})
        pygame.display.update()
        pygame.time.delay(80)
        yield True

    # Sort individual buckets
    for i in range(9):
        if not ascending:
            buckets[i] = sorted(buckets[i], reverse=True)
        else:
            buckets[i] = sorted(buckets[i])

        draw_buckets(buckets, info, 2, {
                     i: info.GRADIENTS3, i+1: info.GRADIENTS4})
        draw_block(info)
        pygame.display.update()
        pygame.time.delay(300)
        yield True

    # Put each element in each bucket back
    k = 0
    for i, arr in enumerate(buckets):
        for j, n in enumerate(arr):
            lst[k] = n
            k += 1
            arr[j] = 0
            draw_buckets(buckets, info, 3, {i: j})
            draw_block(info, {k-1: info.green})
            pygame.display.update()
            pygame.time.delay(80)
            yield True
    return lst


def heapify(arr, n, i, sort_name, info, ascending=True):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if (l < n and arr[largest] < arr[l] and ascending) or (l < n and arr[l] < arr[largest] and not ascending):
        largest = l

    if (r < n and arr[largest] < arr[r] and ascending) or (r < n and arr[r] < arr[largest] and not ascending):
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        if ascending:
            draw_block(info, {
                i: info.GRADIENTS2[0], i+1: info.GRADIENTS2[1], i+2: info.GRADIENTS2[2], largest: info.GRADIENTS4[0]})
        else:
            draw_block(info, {
                i: info.GRADIENTS2[0], i-1: info.GRADIENTS2[1], i-2: info.GRADIENTS2[2], largest-1: info.GRADIENTS4[0]})
        animated(info, 50, sort_name, ascending)
        pygame.display.update()
        pygame.time.delay(70)
        heapify(arr, n, largest, sort_name, info, ascending)


def heap_sort(info, sort_name, ascending=True):
    arr = info.lst
    n = len(arr)
    # Build a maxheap/minheap
    for i in range(int(n / 2) - 1, -1, -1):

        heapify(arr, n, i, sort_name, info, ascending)
        draw_block(info)
        animated(info, 50, sort_name, ascending)
        pygame.display.update()

        yield True

    # One by one extract elements
    for i in range(n-1, 0 if ascending else -1, -1):
        if ascending:
            arr[i], arr[0] = arr[0], arr[i]
        if not ascending:
            arr[0], arr[i] = arr[i], arr[0]

        heapify(arr, i, 0, sort_name, info, ascending)
        draw_block(info, {i if ascending else i-1: info.green, 0: info.red})
        animated(info, 50, sort_name, ascending)
        pygame.display.update()
        pygame.time.delay(70)

        yield True
    return arr


def main():
    run = True

    lst = generate_start_list(60, 0, 100)
    info = Information(lst)

    clock = pygame.time.Clock()
    sorting = False
    ascending = True
    sort_algo = insertion_sort
    sort_name = "Insertion sort"
    sort_generator = None
    index = 2

    while run:
        info.screen.fill((info.background_color))
        clock.tick(24)

        if sorting:
            try:
                next(sort_generator)
            except StopIteration:
                sorting = False
        else:
            if index == 0:
                sort_algo = bubble_sort
                sort_name = "Bubble sort"
            elif index == 1:
                sort_algo = selection_sort
                sort_name = "Selection sort"
            elif index == 2:
                sort_algo = insertion_sort
                sort_name = "Insertion sort"
            elif index == 3:
                sort_algo = heap_sort
                sort_name = "Heap sort"
            elif index == 4:
                sort_algo = bucket_sort
                sort_name = "Bucket sort"
            draw(info, sort_name, ascending)
            draw_star(info, index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_start_list(60, 0, 100)
                info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sort_generator = sort_algo(info, sort_name, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_LEFT and not sorting:
                if index != 0:
                    index -= 1
            elif event.key == pygame.K_RIGHT and not sorting:
                if index != 4:
                    index += 1

        pygame.display.update()


main()
