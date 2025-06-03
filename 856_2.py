from functools import cache

@cache 
def solve(n, face, seen, do_pair):
    """
    Returns expected number of cards drawn before finding first consecutive pair
    """
    if n == 0:
        return float('inf')  # No pair found in deck
        
    cards_drawn = 52 - n
    
    if do_pair:
        # Trying to match the previous card
        match_prob = max(0, 4 - seen) / n
        
        if match_prob > 0:
            # If we match, we've drawn 'cards_drawn' cards before the pair
            return match_prob * cards_drawn + (1 - match_prob) * continue_without_match()
        else:
            return continue_without_match()
            
    # Not trying to pair - draw any card
    expected = 0
    
    for rank in range(13):
        if rank == face:
            # Same rank as previous
            if seen < 4:
                prob = (4 - seen) / n
                expected += prob * solve(n-1, face, seen+1, True)
        else:
            # Different rank
            prob = 4 / n
            expected += prob * solve(n-1, rank, 1, True)
    
    return expected

# To properly handle the recursion:
@cache
def solve(n, face, seen):
    """
    Returns expected cards before first consecutive pair
    when we have n cards left, previous card was rank 'face',
    and we've seen 'seen' cards of that rank
    """
    if n == 0:
        return float('inf')
        
    cards_drawn = 52 - n
    
    # Probability next card matches
    match_prob = max(0, 4 - seen) / n
    
    if match_prob > 0:
        # If match: we've drawn 'cards_drawn' cards before the pair
        expected_if_match = cards_drawn
        
        # If no match: we draw this card and continue
        expected_if_no_match = 0
        for rank in range(13):
            if rank == face:
                if seen < 4:
                    prob = (4 - seen) / n  
                    # This would be a match, skip
                    continue
            else:
                prob = 4 / n
                expected_if_no_match += prob * (1 + solve(n-1, rank, 1))
                
        # Normalize probabilities for non-match case
        if (1 - match_prob) > 0:
            expected_if_no_match /= (1 - match_prob)
            
        return match_prob * expected_if_match + (1 - match_prob) * expected_if_no_match
    else:
        # Can't match, must draw different rank
        expected = 0
        for rank in range(13):
            if rank != face:
                prob = 4 / n
                expected += prob * (1 + solve(n-1, rank, 1))
        return expected

# Start: first card can be any rank
expected = 0
for rank in range(13):
    prob = 4 / 52
    expected += prob * solve(51, rank, 1)

print(f"Expected cards before first consecutive pair: {expected}")