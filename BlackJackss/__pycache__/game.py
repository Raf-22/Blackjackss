import random

suits = ['Cuori', 'Quadri', 'Fiori', 'Picche']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
          '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def filename(self):
        return f"{self.rank}{self.suit}.png"


class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
class Wallet:
    def __init__(self):
        self.balance = 0

    def set_balance(self, amount):
        self.balance = amount

    def update_balance(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

class BetManager:
    def __init__(self, wallet):
        self.wallet = wallet
        self.bet = 0

    def place_bet(self, amount):
        if amount > self.wallet.get_balance():
            return False 
        self.bet = amount
        self.wallet.update_balance(-amount)
        return True

    def reset_bet(self):
        self.bet = 0


class BlackjackGame:
    def __init__(self):
        self.wallet = Wallet()  
        self.bet_manager = BetManager(self.wallet) 
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.result = ""
        self.over = False

        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.wallet.set_balance(1000)  

    def hit(self):
        """Metodo per chiedere una carta in più"""
        if not self.over:
            self.player_hand.add_card(self.deck.deal())
            if self.player_hand.get_value() > 21:
                self.result = "Hai sballato!"
                self.over = True

    def stand(self):
        """Metodo per fermarsi e far giocare il mazziere"""
        if self.over:
            return
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())

        player = self.player_hand.get_value()
        dealer = self.dealer_hand.get_value()

        if dealer > 21 or player > dealer:
            self.result = "Hai vinto!"
            self.wallet.update_balance(self.bet_manager.bet * 2)  
        elif dealer > player:
            self.result = "Hai perso!"
        else:
            self.result = "Pareggio!"

        self.over = True
        self.bet_manager.reset_bet() 
    def restart(self):
        """Metodo per iniziare una nuova partita"""
        self.__init__()

    def place_bet(self, amount):
        """Piazza la puntata (verifica se il saldo è sufficiente)"""
        if not self.bet_manager.place_bet(amount):
            self.result = "Puntata troppo alta!"
        else:
            self.result = f"Puntata di {amount} limoni effettuata!"

    def get_player_hand_value(self):
        return self.player_hand.get_value()

    def get_dealer_hand_value(self):
        return self.dealer_hand.get_value()

    def get_balance(self):
        """Restituisce il saldo attuale del giocatore"""
        return self.wallet.get_balance()

    def get_result(self):
        """Restituisce il risultato finale della partita"""
        return self.result
