from game import Game

def main():
    NUM_PLAYERS = 8
    skyjo = Game(NUM_PLAYERS)
    print(f"New game started with {NUM_PLAYERS} players.")
    
    round_number = 1
    while not skyjo.is_game_over():
        print(f"\nRound {round_number}")
        skyjo.init_round()
        
        round_finisher = None
        # Play until someone finishes the round
        while round_finisher is None and skyjo.deck:
            for player in skyjo.players:
                if skyjo.deck:
                    skyjo.playable_card = player.play_turn(skyjo.playable_card)
                    #skyjo.playable_card = player.play_turn(skyjo.deck.pop(0))
                
                round_finisher = skyjo.get_round_finisher()
                if round_finisher:                    
                    break
        
        # One final turn for others if someone finished
        if round_finisher:
            print(f"{round_finisher.name} finished the round")
            for player in skyjo.reorder_players(round_finisher)[1:]:
                player.play_turn(skyjo.deck.pop(0))
        else:
            print("no card left in deck", len(skyjo.deck))
        
        skyjo.update_scores()
        
        # Display round results
        print(f"\nRound {round_number} Results:")
        for player in skyjo.players:
            print(f"{player}: {player.score} points")
        
        round_number += 1
    
    # Display final game results
    print("\nGame Over!")
    print("Final Scores:")
    for player in sorted(skyjo.players, key=lambda p: p.score):
        print(f"{player}: {player.score} points")
    
    winner = skyjo.get_game_winner()
    if winner:
        print(f"\nThe winner is {winner} with {winner.score} points!")
    else:
        print("\nNo winner determined.")

if __name__ == "__main__":
    main()