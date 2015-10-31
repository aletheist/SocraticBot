import toolz
from pprint import pprint
import praw
import core

def is_question(comment):
    """Heuristically determine if a post is quesiton."""
    return '?' in str(comment)

def is_answer(comment):
    """Heuristically determine if a post is an answer."""
    return '?' not in str(comment)

def find_potential_violations(comments):
    threads = [core.get_threads(comment) for comment in comments]
    for thread in threads:
        for branch in thread:
            for expected_answer, expected_question in toolz.partition(2, branch):
                if not is_answer(expected_answer):
                    yield expected_answer
                if not is_question(expected_question):
                    yield expected_question

if __name__ == "__main__":
    reddit = praw.Reddit('Socrates', '')
    submission = reddit.get_submission(submission_id='3qmlvv')
    submission.replace_more_comments()
    reported_comments = find_potential_violations(submission.comments)
    pprint(sorted(map(str, reported_comments)))
