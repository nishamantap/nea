import pygame
import random

pygame.init()

Width = 800
Height = 600
surface = pygame.display.set_mode((Width, Height))

DFLT_IMG_SZ = (50, 70)

button_surface = pygame.Surface((140, 50))
button_rect = pygame.Rect(500, 180, 180, 180)

# Card game initialization
class CardGame:
    def __init__(self):
        self.images_paths = ['ace_of_diamonds.png', 'ace_of_spades.png', 'ace_of_hearts.png', 'ace_of_clubs.png',
                        '2_of_diamonds.png', '2_of_spades.png', '2_of_hearts.png', '2_of_clubs.png',
                        '3_of_diamonds.png', '3_of_spades.png', '3_of_hearts.png', '3_of_clubs.png',
                        '4_of_diamonds.png', '4_of_spades.png', '4_of_hearts.png', '4_of_clubs.png',
                        '5_of_diamonds.png', '5_of_spades.png', '5_of_hearts.png', '5_of_clubs.png',
                        '6_of_diamonds.png', '6_of_spades.png', '6_of_hearts.png', '6_of_clubs.png',
                        '7_of_diamonds.png', '7_of_spades.png', '7_of_hearts.png', '7_of_clubs.png',
                        '8_of_diamonds.png', '8_of_spades.png', '8_of_hearts.png', '8_of_clubs.png',
                        '9_of_diamonds.png', '9_of_spades.png', '9_of_hearts.png', '9_of_clubs.png',
                        '10_of_diamonds.png', '10_of_spades.png', '10_of_hearts.png', '10_of_clubs.png',
                        'jack_of_diamonds.png', 'jack_of_spades.png', 'jack_of_hearts.png', 'jack_of_clubs.png',
                        'queen_of_diamonds.png', 'queen_of_spades.png', 'queen_of_hearts.png', 'queen_of_clubs.png',
                        'king_of_diamonds.png', 'king_of_spades.png', 'king_of_hearts.png', 'king_of_clubs.png']
        self.images = [pygame.transform.scale(pygame.image.load(image_path), DFLT_IMG_SZ) for image_path in
                   self.images_paths]

        self.shuffle_cards()
        self.players = 2  # Number of players

    def shuffle_cards(self):
        random.shuffle(self.images)

    def deal_card(self):
        return self.images.pop(0)  # Pop the first card from the list

    def update_positions(self):
        positions_top = []
        positions_bottom = []
        num_cards = len(self.images)
        cards_per_row = num_cards // 4  # Assuming 4 cards per row
        start_x_top = (Width - (cards_per_row * DFLT_IMG_SZ[0] + (cards_per_row - 1) * 10)) // 2
        start_x_bottom = (Width - (cards_per_row * DFLT_IMG_SZ[0] + (cards_per_row - 1) * 10)) // 2
        x_top, x_bottom, y_top, y_bottom = start_x_top, start_x_bottom, 50, Height - 2*DFLT_IMG_SZ[1] - 50
        player_index = 0
        for i, card in enumerate(self.images):
            if i < num_cards // 2:
                positions_top.append((x_top, y_top, player_index))
                x_top += DFLT_IMG_SZ[0] + 10
                if (i + 1) % cards_per_row == 0:
                    y_top += DFLT_IMG_SZ[1] + 10
                    x_top = start_x_top
            else:
                positions_bottom.append((x_bottom, y_bottom, player_index))
                x_bottom += DFLT_IMG_SZ[0] + 10
                if (i - num_cards // 2 + 1) % cards_per_row == 0:
                    y_bottom += DFLT_IMG_SZ[1] + 10
                    x_bottom = start_x_bottom

        return positions_top, positions_bottom


game = CardGame()

run = True
selected_card = None  # Variable to store the selected card
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                game.shuffle_cards()
                game.images.append(game.images.pop(0))  # Move the top card to the bottom
                card = game.deal_card()
                surface.blit(card, (100, 150))  # Blit the new top card
            else:
                # Check if any card was clicked
                card_positions_top, card_positions_bottom = game.update_positions()
                for i, pos in enumerate(card_positions_top):
                    x, y, _ = pos
                    if x <= event.pos[0] <= x + DFLT_IMG_SZ[0] and y <= event.pos[1] <= y + DFLT_IMG_SZ[1]:
                        selected_card = game.images.pop(i)  # Remove the selected card from the game
                        break
                for i, pos in enumerate(card_positions_bottom):
                    x, y, _ = pos
                    if x <= event.pos[0] <= x + DFLT_IMG_SZ[0] and y <= event.pos[1] <= y + DFLT_IMG_SZ[1]:
                        selected_card = game.images.pop(len(card_positions_top) + i)  # Remove the selected card from the game
                        break

    surface.fill((14, 144, 44))  # Fill the surface with a green background

    card_positions_top, card_positions_bottom = game.update_positions()
    for card, pos in zip(game.images[:len(card_positions_top)], card_positions_top):
        x, y, player_index = pos
        surface.blit(card, (x, y))
    for card, pos in zip(game.images[len(card_positions_top):], card_positions_bottom):
        x, y, player_index = pos
        surface.blit(card, (x, y))

    # Display the selected card in the middle of the window if one is selected
    if selected_card:
        surface.blit(selected_card, ((Width - DFLT_IMG_SZ[0]) // 2, (Height - DFLT_IMG_SZ[1]) // 2))

    surface.blit(button_surface, (button_rect.x, button_rect.y))

    pygame.display.update()

pygame.quit()

