from datetime import date

def calculate_score(user, used_hint: bool, correct_year: bool):
    base = 1 if used_hint else 2
    score = base + user.streak  # streak adds +1 for each prior correct
    if correct_year:
        score += 1
    return score

def update_user_on_success(user, score: int):
    user.total_score += score
    user.streak += 1
    user.last_score = score

def update_user_on_failure(user):
    user.lives_remaining -= 1
    user.streak = 0
    user.last_score = 2