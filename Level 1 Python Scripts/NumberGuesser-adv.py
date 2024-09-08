import random
min = int(input("Enter the minimum value: "))
max = int(input("Enter the maximum value: "))
attempts = 6
win = False
first_try = False
number = random.randint(min, max)
last_hint = f"{'EVEN' if number%2 ==0 else 'ODD'}"

#game instructions
def game_start():
    print(f"I am thinking of a number between {min} and {max}")
    print(f"If you can guess that number exactly (within {attempts} times), then I wil pay out that amount. OK?")
    input("Press ENTER to try your meddle at this game...")

#processing user input
def game_play():
    global number, attempts, last_hint, win, first_try
    max_guess = attempts
    while attempts > 0:
        print()
        print(f"You have {attempts} {'attempts' if attempts > 1 else 'attempts'} left.")
        
        if attempts == 1:
            print(f"Final call. Here's your final hint: It's a {last_hint} number.")
        
        while True:
            try:
                guess = int(input("Try a lucky number: "))
                if guess in range(min, max+1):
                    break
                else:
                    print(f"Please try and keep it between {min} and {max} Thanks!")
            except ValueError:
                print()
                print("Oops looks like those aren't numbers there!")
        if guess == number:
            win = True
            if max_guess == attempts:
                first_try = True
            break
        if guess == 1:
            break
        if guess > number:
            if guess-number > 5:
                print("Going too big there. Try thinking smaller.")
            else:
                print("Oh my! You're getting close. A bit smaller and you'll probably get it!")
        attempts -= 1


#printing the end game results
def game_finish(win, first_try):
    if win:
        if first_try:
            print("Well now, you've got it on the first go of this. You must be a genius!")
            print(f"Here is an additional ${number//2} plus ${number} since you've got it right!")
        else:
            print(f"Congratulations! You guessed it right. Now it's time to accept your prize of that amount! Total amount due is ${number}.")
    else:
        print(f"The lucky number is {number}. \nSorry to say, but you've lost this time.")



if __name__ == '__main__':
    game_start()
    game_play()
    game_finish(win, first_try)
    
