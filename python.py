"""AIXcelerate Task 1: Mood Guesser (Happy or Sad)."""

import string

train_data = [
    ("I got full marks in the test today!", "Happy"),
    ("We won the college cricket match", "Happy"),
    ("My friends planned a surprise party for me", "Happy"),
    ("The food in the canteen was really tasty", "Happy"),
    ("I am so excited for the weekend trip", "Happy"),
    ("Our project got selected for the exhibition", "Happy"),
    ("I finally learned how to ride a bicycle", "Happy"),
    ("Mom made my favourite sweets today", "Happy"),
    ("I lost my phone on the bus", "Sad"),
    ("I failed in the mathematics exam", "Sad"),
    ("My best friend is moving to another city", "Sad"),
    ("It rained and our picnic was cancelled", "Sad"),
    ("I missed the last bus and felt very upset", "Sad"),
    ("My laptop stopped working before the submission", "Sad"),
    ("I felt lonely during the long holidays", "Sad"),
]

practice_data = [
    ("I won a medal in the sports meet", "Happy"),
    ("I lost my notebook before the exam", "Sad"),
    ("My friends gave me a lovely surprise", "Happy"),
    ("The train was late and I felt upset", "Sad"),
    ("Today was a great day", "Happy"),
]


# ---------------------------------------------------------------
# Level 1: Count the moods
# ---------------------------------------------------------------
def count_moods(data):
    """Return (number of Happy, number of Sad) for any list in the same format."""
    happy_count = 0
    sad_count = 0
    for sentence, mood in data:
        if mood == "Happy":
            happy_count += 1
        elif mood == "Sad":
            sad_count += 1
    return happy_count, sad_count


# ---------------------------------------------------------------
# Level 2: Guess the mood with clue words
# ---------------------------------------------------------------
# N = last digit of roll number (use 10 if the last digit is 0).
# CHANGE THIS NUMBER to your own N. Each list below keeps exactly N words.
N = 5

# Words are ordered from most useful to least useful, so cutting to N
# keeps the best ones.
happy_words = ["won", "surprise", "great", "lovely", "excited",
               "favourite", "tasty", "selected", "learned", "marks"][:N]
sad_words = ["lost", "upset", "failed", "missed", "cancelled",
             "lonely", "stopped", "moving", "rained", "sad"][:N]


def clean_words(sentence):
    """Lowercase the sentence, remove punctuation, and split into words."""
    sentence = sentence.lower()
    for ch in string.punctuation:
        sentence = sentence.replace(ch, "")
    return sentence.split()


def guess_mood(sentence):
    """Return exactly "Happy" or "Sad" by counting clue words."""
    happy_score = 0
    sad_score = 0
    for word in clean_words(sentence):
        if word in happy_words:
            happy_score += 1
        if word in sad_words:
            sad_score += 1
    if happy_score > sad_score:
        return "Happy"
    if sad_score > happy_score:
        return "Sad"
    # Tie (including no clue words): choose Happy, because Happy is the
    # majority in the training data (8 Happy vs 7 Sad).
    return "Happy"


# ---------------------------------------------------------------
# Bonus: learn the word scores from examples
# ---------------------------------------------------------------
def learn_scores(data):
    """Score = (times in Happy sentences) - (times in Sad sentences)."""
    scores = {}
    for sentence, mood in data:
        for word in clean_words(sentence):
            if word not in scores:
                scores[word] = 0
            if mood == "Happy":
                scores[word] += 1
            else:
                scores[word] -= 1
    return scores


learned_scores = learn_scores(train_data)


def guess_mood_learned(sentence):
    """Add up the learned scores. Positive total = Happy, otherwise Sad.
    Unseen words score 0."""
    total = 0
    for word in clean_words(sentence):
        total += learned_scores.get(word, 0)
    if total > 0:
        return "Happy"
    return "Sad"


def accuracy(data, guesser):
    """Percentage of sentences the guesser gets right."""
    correct = 0
    for sentence, mood in data:
        if guesser(sentence) == mood:
            correct += 1
    return correct / len(data) * 100


# ---------------------------------------------------------------
# Level 3: Test the program
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("Level 1:", count_moods(train_data))  # should be (8, 7)
    print("happy_words:", happy_words)
    print("sad_words:", sad_words)

    print("\nLevel 3: practice sentences")
    for sentence, real in practice_data:
        print(f"{sentence!r} -> guessed {guess_mood(sentence)}, real {real}")
    print(f"Level 2 accuracy: {accuracy(practice_data, guess_mood):.0f} %")

    print("\nBonus: learned scores")
    for sentence, real in practice_data:
        print(f"{sentence!r} -> guessed {guess_mood_learned(sentence)}, real {real}")
    print(f"Learned accuracy: {accuracy(practice_data, guess_mood_learned):.0f} %")

    # Learning note questions (worked by code)
    note_scores = {"good": 2, "party": 1, "exam": 0, "bad": -2, "day": -1}
    for text in ["good party today", "bad exam day"]:
        total = sum(note_scores.get(w, 0) for w in text.split())
        print(f"Note score of {text!r}: {total}")
