from __future__ import annotations

import html
import random

import requests

API_ROOT = "https://opentdb.com/api.php"
REQUEST_TIMEOUT = 30


def unescape_result(result: dict) -> dict:
    return {
        **result,
        "question": html.unescape(result["question"]),
        "correct_answer": html.unescape(result["correct_answer"]),
        "incorrect_answers": [html.unescape(a) for a in result["incorrect_answers"]],
    }


def answer_matches(user: str, expected: str) -> bool:
    """Case- and surrounding-whitespace-insensitive comparison (True vs true, etc.)."""
    return user.strip().casefold() == expected.strip().casefold()


def boolean_questions(result: dict, answers: list[str]) -> int:
    print(result['question'])
    print(answers)
    user_input = input('What is the answer? (True/False): ')
    if answer_matches(user_input, result['correct_answer']):
        print('Correct')
        return 1
    elif answer_matches(user_input, result['incorrect_answers'][0]):
        print('Wrong, the correct answer was', result['correct_answer'])
        return 0
    else:
        print('Choose a valid answer')
        return boolean_questions(result, answers)


def multiple_questions(result: dict, answers: list[str]) -> int:
    print(result['question'])
    print(answers)
    user_input = input('What is the answer?: ')
    if answer_matches(user_input, result['correct_answer']):
        print('Correct')
        return 1
    elif any(
        answer_matches(user_input, wrong) for wrong in result['incorrect_answers']
    ):
        print('Wrong, the correct answer was', result['correct_answer'])
        return 0
    else:
        print('Choose a valid answer')
        return multiple_questions(result, answers)


def main(amount: int, difficulty: str) -> int:
    response = requests.get(
        API_ROOT,
        params={"amount": amount, "category": 27, "difficulty": difficulty},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("response_code", 0) != 0:
        print(
            "Could not load questions (Open Trivia API response_code:",
            data.get("response_code"),
            "). Try fewer questions or another difficulty.",
        )
        return 0
    results = data['results']
    score = 0
    for raw in results:
        result = unescape_result(raw)
        answers = []
        answers.append(result['correct_answer'])
        for option in result['incorrect_answers']:
            answers.append(option)

        random.shuffle(answers)

        if result['type'] == 'boolean':
            question_score = boolean_questions(result, answers)
            score += question_score
        else:
            question_score = multiple_questions(result, answers)
            score += question_score
    return score
    
if __name__ == "__main__":
    amount_raw = input("How many questions would you like? ").strip()
    difficulty = input(
        "How difficult do you want the questions? (easy, medium, hard): "
    ).strip().lower()
    if amount_raw.isdigit() and int(amount_raw) > 0 and difficulty in (
        "easy",
        "medium",
        "hard",
    ):
        amount = int(amount_raw)
        score = main(amount, difficulty)
        print("You scored", score, "/", amount)
    else:
        print("Enter a positive whole number and difficulty: easy, medium, or hard.")