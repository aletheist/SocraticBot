from pprint import pprint
import praw
import core

class QaChecker(object):
    def __init__(self):
        self.reported_comments = set()

    def check(self, comments):
        for c in comments:
            if '?' in str(c):
                current_type = '?'
                self.reported_comments.add(c)
            else:
                current_type = '.'
            for r in c.replies:
                self.recursive_check(r, current_type)

    def recursive_check(self, comment, last_type):
        if '?' in str(comment):
            current_type = '?'
        else:
            current_type = '.'
        if last_type == current_type:
            self.reported_comments.add(comment)
        for c in comment.replies:
            self.recursive_check(c, current_type)

def is_question(comment):
    return '?' in str(comment)

def is_answer(comment):
    return '?' not in str(comment)

def qa_check(comments):
    threads = [core.get_threads(comment) for comment in comments]
    for thread in threads:
        for branch in thread:
            branch = tuple(branch)
            for comment in branch[1::2]:
                if is_answer(comment):
                    yield comment
            for comment in branch[::2]:
                if is_question(comment):
                    yield comment

def qa_check2(comments):
    checker = QaChecker()
    checker.check(comments)
    return checker.reported_comments

if __name__ == "__main__":
    reddit = praw.Reddit('Socrates', '')
    submission = reddit.get_submission(submission_id='3qmlvv')
    submission.replace_more_comments()
    reported_comments = qa_check(submission.comments)
    reported_comments2 = qa_check2(submission.comments)
    pprint(sorted(map(str, reported_comments2)))
    pprint(sorted(map(str, reported_comments)))
