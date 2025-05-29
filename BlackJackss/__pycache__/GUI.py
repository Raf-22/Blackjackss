import pygame
import os
from game import BlackjackGame

class BlackjackGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Blackjack per ballarti la fresca")

        icon = pygame.image.load(os.path.join("Img", "Icona.png"))
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("verdana", 24, bold=True)
        self.large_font = pygame.font.SysFont("verdana", 48, bold=True)
        self.running = True
        self.game = None
        self.card_images = {}
        self.back_image = pygame.image.load(os.path.join("Img", "Dorso.png"))
        self.table_image = pygame.image.load(os.path.join("Img", "table_background.jpg"))
        self.menu_background = pygame.image.load(os.path.join("Img", "SfondoMenù.png"))
        self.load_images()
        self.state = "menu"
        self.dropdown_open = False

    def load_images(self):
        for suit in ['Cuori', 'Quadri', 'Fiori', 'Picche']:
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                name = f"{rank}{suit}.jpg"
                path = os.path.join("Img", name)
                if os.path.exists(path):
                    self.card_images[f"{rank}{suit}"] = pygame.image.load(path)
                else:
                    print(f"Immagine mancante: {path}")

    def draw_card(self, card, x, y):
        key = f"{card.rank}{card.suit}"
        image = self.card_images.get(key)
        if image:
            self.screen.blit(pygame.transform.scale(image, (80, 120)), (x, y))

    def draw_button(self, rect, text, hover=False):
        base_color = (139, 0, 0)
        hover_color = (178, 34, 34)
        color = hover if hover else base_color
        pygame.draw.rect(self.screen, hover_color if hover else base_color, rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 215, 0), rect, 3, border_radius=15)
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

    def show_menu(self):
        self.screen.blit(pygame.transform.scale(self.menu_background, (1000, 700)), (0, 0))
        title_text = " Blackjacksss "
        shadow = self.large_font.render(title_text, True, (0, 0, 0))
        title = self.large_font.render(title_text, True, (255, 215, 0))

        title_x = self.screen.get_width() // 2 - title.get_width() // 2
        title_y = 100
        self.screen.blit(shadow, (title_x + 2, title_y + 2))
        self.screen.blit(title, (title_x, title_y))

        start_btn = pygame.Rect(400, 260, 200, 60)
        rules_btn = pygame.Rect(400, 340, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(start_btn, "Inizia partita", start_btn.collidepoint(mouse_pos))
        self.draw_button(rules_btn, "Regole", rules_btn.collidepoint(mouse_pos))

        return {"start": start_btn, "rules": rules_btn}

    def show_rules(self):
        self.screen.fill((10, 10, 10))
        title = self.large_font.render("Regole del Blackjack", True, (255, 215, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))
        lines = [
            "- Arriva a 21 senza sballare",
            "- Il mazziere pesca fino a 17",
            "- Puoi chiedere carta o stare",
            "- Le carte numeriche valgono il loro numero ",
            "- J, Q, K valgono 10 punti.",
            "- L'Asso vale 1 o 11, a seconda di cosa conviene al giocatore.",
            "- Se hai un Asso + una carta da 10 punti hai un Blackjack.",
            "- I veri giocatori non mollano mai prima della grande vincita",
        ]
        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(rendered, (120, 150 + i * 40))

        back_btn = pygame.Rect(400, 500, 200, 60)
        self.draw_button(back_btn, "Torna indietro", back_btn.collidepoint(pygame.mouse.get_pos()))
        return back_btn

    def show_game(self):
        self.screen.blit(pygame.transform.scale(self.table_image, (1000, 700)), (0, 0))
        if not self.game:
            return

        title = self.large_font.render("GIOCA VINCI E RIGIOCA!", True, (255, 215, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 20))

        for i, card in enumerate(self.game.dealer_hand.cards if self.game.over else [self.game.dealer_hand.cards[0]]):
            x = 400 + i * 30
            if self.game.over or i == 0:
                self.draw_card(card, x, 150)
            else:
                self.screen.blit(self.back_image, (x, 150))

        if self.game.over:
            dealer_val = self.font.render(f"Mazziere: {self.game.dealer_hand.get_value()}", True, (255, 255, 255))
            self.screen.blit(dealer_val, (400, 120))

        for i, card in enumerate(self.game.player_hand.cards):
            self.draw_card(card, 400 + i * 30, 400)

        player_val = self.font.render(f"Giocatore: {self.game.player_hand.get_value()}", True, (255, 255, 255))
        self.screen.blit(player_val, (400, 370))

       
        hit_btn = pygame.Rect(100, 600, 150, 50)
        stand_btn = pygame.Rect(300, 600, 150, 50)
        restart_btn = pygame.Rect(550, 600, 180, 50)

        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(hit_btn, "Carta", hit_btn.collidepoint(mouse_pos))
        self.draw_button(stand_btn, "Stai", stand_btn.collidepoint(mouse_pos))
        self.draw_button(restart_btn, "Ricomincia", restart_btn.collidepoint(mouse_pos))

       
        bet_btn = pygame.Rect(800, 600, 150, 50)
        self.draw_button(bet_btn, "Puntata", bet_btn.collidepoint(mouse_pos))

        
        if self.game.over:
            result = self.large_font.render(self.game.result, True, (255, 215, 0))
            self.screen.blit(result, (self.screen.get_width() // 2 - result.get_width() // 2, 300))

        saldo_text = f"Saldo: {self.game.wallet.balance}"
        saldo_label = self.font.render(saldo_text, True, (255, 215, 0))  
        saldo_label_rect = saldo_label.get_rect(midleft=(50, self.screen.get_height() // 2))
        self.screen.blit(saldo_label, saldo_label_rect)

        return {"hit": hit_btn, "stand": stand_btn, "restart": restart_btn, "bet": bet_btn}

    def show_dropdown_menu(self):
        if self.state != "game":
            return {}

        menu_icon = pygame.Rect(930, 10, 50, 40)
        line_y = menu_icon.y + 10
        for _ in range(3):
            pygame.draw.rect(self.screen, (255, 255, 255), (menu_icon.x + 10, line_y, 30, 4))
            line_y += 10

        buttons = {"menu_icon": menu_icon}

        if self.dropdown_open:
            modal = pygame.Rect(300, 200, 400, 300)
            pygame.draw.rect(self.screen, (30, 30, 30), modal, border_radius=10)
            pygame.draw.rect(self.screen, (255, 215, 0), modal, 3, border_radius=10)

            resume_btn = pygame.Rect(350, 240, 300, 50)
            menu_btn = pygame.Rect(350, 310, 300, 50)
            rules_btn = pygame.Rect(350, 380, 300, 50)

            mouse_pos = pygame.mouse.get_pos()
            self.draw_button(resume_btn, "Riprendi", resume_btn.collidepoint(mouse_pos))
            self.draw_button(menu_btn, "Torna al menù", menu_btn.collidepoint(mouse_pos))
            self.draw_button(rules_btn, "Regole", rules_btn.collidepoint(mouse_pos))

            buttons.update({
                "resume": resume_btn,
                "menu": menu_btn,
                "rules": rules_btn
            })

        return buttons

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            buttons = {}

            if self.state == "menu":
                buttons = self.show_menu()
            elif self.state == "rules":
                back_btn = self.show_rules()
            elif self.state == "game":
                buttons = self.show_game()

            dropdown_buttons = self.show_dropdown_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu":
                        if buttons["start"].collidepoint(event.pos):
                            self.game = BlackjackGame()
                            self.state = "game"
                        elif buttons["rules"].collidepoint(event.pos):
                            self.state = "rules"
                    elif self.state == "rules":
                        if back_btn.collidepoint(event.pos):
                            self.state = "menu"
                    elif self.state == "game":
                        if buttons.get("hit") and buttons["hit"].collidepoint(event.pos):
                            self.game.hit()
                        elif buttons.get("stand") and buttons["stand"].collidepoint(event.pos):
                            self.game.stand()
                        elif buttons.get("restart") and buttons["restart"].collidepoint(event.pos):
                            self.game.restart()

                        if dropdown_buttons.get("menu_icon") and dropdown_buttons["menu_icon"].collidepoint(event.pos):
                            self.dropdown_open = not self.dropdown_open

                        if self.dropdown_open:
                            if dropdown_buttons.get("resume") and dropdown_buttons["resume"].collidepoint(event.pos):
                                self.dropdown_open = False
                            elif dropdown_buttons.get("menu") and dropdown_buttons["menu"].collidepoint(event.pos):
                                self.state = "menu"
                                self.dropdown_open = False
                            elif dropdown_buttons.get("rules") and dropdown_buttons["rules"].collidepoint(event.pos):
                                self.state = "rules"
                                self.dropdown_open = False

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
