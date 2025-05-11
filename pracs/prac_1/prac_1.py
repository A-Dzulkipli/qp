import random
import numpy as np
from scipy.stats import invgamma

class CoinGame:
    def __init__(self):
        self.coins = self.choose_distribution()
        self.moves = 100
        self.score = 0
        self.history = [0]*10
        self.success = [0]*10
    
    def select_coin(self, n):
        r = random.random()
        if r < self.coins[n]:
            return True
        return False
    
    def get_int(self):
        while True:
            try:
                return int(input("Select Coin: "))
            except ValueError:
                print("Please enter an integer")
    
    def play_game(self):
        while (self.moves > 0):
            print(f"Moves Remaining: {self.moves}")
            move_history = [f"{self.success[i]} / {self.history[i]}" for i in range(10)]

            print(f"Success Rate: {move_history}")
            coin = self.get_int()
            while coin < 0 or coin > 9:
                print("Coins only go from 0 to 9")
                coin = self.get_int()
            outcome = self.select_coin(coin)
            if outcome:
                print("success")
                self.score += 1
                self.success[coin] += 1
            else:
                print("fail")
            self.history[coin] += 1
            self.moves -= 1

        
        print(f"Score: {self.score}")
        print(f"Coin Distribution: {self.coins}")

    def select_uniform(self):
        coins = [random.random() for _ in range(9)]
        coins.append(0.5)
        random.shuffle(coins)

        return coins
    
    def get_std(self):
        std = invgamma.rvs(a=5, scale=1)
        while std > 1/3:
            std = invgamma.rvs(a=5, scale=1)
        return std
    
    def select_normal(self):
        std = self.get_std()
        mean = 0.5

        coins = [0.5]

        while len(coins) < 10:
            x = np.random.normal(loc=mean, scale=std)
            if x > 0 and x < 1:
                coins.append(x)
        random.shuffle(coins)
        return coins
    
    def select_zero(self):
        coins = [0]*9
        coins.append(0.5)
        random.shuffle(coins)
        return coins

    def select_bimodal(self):
        mean_1 = np.random.normal(loc=0.8, scale=0.05)
        mean_2 = np.random.normal(loc=0.2, scale=0.05)

        coins = []

        for _ in range(5):
            r = np.random.normal(loc=mean_1, scale=0.05)
            while r <= 0 or r >= 1:
                r = np.random.normal(loc=mean_1, scale=0.05)
            coins.append(r)

            r = np.random.normal(loc=mean_2, scale=0.05)
            while r <= 0 or r >= 1:
                r = np.random.normal(loc=mean_2, scale=0.05)
            coins.append(r)

        random.shuffle(coins)
        coins[0] = 0.5
        random.shuffle(coins)
        return coins
    


    def choose_distribution(self):
        distributions = {
            0: self.select_uniform,
            1: self.select_bimodal,
            2: self.select_normal,
            3: self.select_zero
        }

        coins = distributions[random.randint(0,3)]()
        return coins
    
    def setup(self):
        self.coins = self.choose_distribution()
        self.moves = 100
        self.score = 0
        self.history = [0]*10
        self.success = [0]*10

    def choose_coin(self, coin: int):
        if self.moves == 0:
            return [self.moves, self.score, self.history, self.success]
        if coin < 0 or coin > 9:
            return -1
        else:
            r = random.random()
            if r < self.coins[coin]:
                self.score += 1
                outcome = 1
                self.success[coin] += 1
            else:
                outcome = 0
            self.history[coin] += 1
            self.moves -= 1
            return [outcome, self.moves, self.score, self.history, self.success]


def main():
    coin_game = CoinGame()
    coin_game.play_game()
    # print(coin_game.get_std())

if __name__ == "__main__":
    main()