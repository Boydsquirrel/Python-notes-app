import pygame  # Import the Pygame library

pygame.init()  # Initialize all imported Pygame modules

# Set up the game window (200x75 pixels)
screen = pygame.display.set_mode((200, 75))
pygame.display.set_caption('Note taker')
font = pygame.font.Font(None, size=20)

# Input box setup
input_box = pygame.Rect(5, 20, 190, 40)
color_active = pygame.Color('dodgerblue2')
color_inactive = pygame.Color('lightskyblue3')
color = color_inactive
active = False
text = ''
cursor_pos = 0
blink = True
blink_timer = 0

clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    screen.fill((255, 255, 133))  # Fill background with notepad colour

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            active = input_box.collidepoint(event.pos)
            color = color_active if active else color_inactive

        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE and cursor_pos > 0:
                text = text[:cursor_pos-1] + text[cursor_pos:]
                cursor_pos -= 1
            elif event.key == pygame.K_LEFT:
                cursor_pos = max(cursor_pos - 1, 0)
            elif event.key == pygame.K_RIGHT:
                cursor_pos = min(cursor_pos + 1, len(text))
            elif event.key == pygame.K_RETURN:
                print("Entered:", text)
                text = ''
                cursor_pos = 0
            else:
                if event.unicode.isprintable():
                    text = text[:cursor_pos] + event.unicode + text[cursor_pos:]
                    cursor_pos += 1

    # Render the text inside the input box
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 8))

    # Draw input box rectangle
    pygame.draw.rect(screen, color, input_box, 2)

    # Cursor blinking logic
    blink_timer += 1
    if blink_timer % 60 == 0:
        blink = not blink
    if blink and active:
        cursor_x = input_box.x + 5 + font.size(text[:cursor_pos])[0]
        pygame.draw.line(screen, color, (cursor_x, input_box.y + 8), (cursor_x, input_box.y + input_box.height - 8), 2)

    pygame.display.flip()  # Update the screen

    # Control frame rate
    delta_time = clock.tick(60) / 1000.0
    delta_time = max(0.001, min(0.1, delta_time))  # Clamp to prevent big jumps

pygame.quit()
