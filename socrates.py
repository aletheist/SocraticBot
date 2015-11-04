import itertools
import toolz
from pprint import pprint
import praw

def get_threads(comment):
    """
    Given a root comment, return a list of the 'branches' or 'threads of
    discussion' for it. For example:

        comment 1
            commetn 2
            comment 3
                comment 4

    will return:

         [comment 1, comment 2]
         [comment 1, comment 3, comment 4]
    """

    if not comment.replies:
        yield [comment]
    for reply in comment.replies:
        if not reply.replies:
            yield [comment, reply]
        else:
            for r in get_threads(reply):
                yield [comment] + r

def is_question(comment):
    """Heuristically determine if a post is quesiton."""
    return '?' in str(comment)

def is_answer(comment):
    """Heuristically determine if a post is an answer."""
    return '?' not in str(comment)

def find_potential_violations(branch):
    expected_answers = itertools.islice(branch, None, None, 2)
    expected_questions = itertools.islice(branch, 1, None, 2)
    return toolz.concatv(filter(is_question, expected_answers),
                         filter(is_answer, expected_questions))

if __name__ == "__main__":
    reddit = praw.Reddit('Socrates', '')
    submission = reddit.get_submission(submission_id='3qmlvv')
    submission.replace_more_comments()
    threads = [get_threads(comment) for comment in submission.comments]
    reported_comments = []
    for thread in threads:
        for branch in thread:
            reported_comments += find_potential_violations(branch)
    for comment in sorted(reported_comments):
        print str(comment), comment.permalink
