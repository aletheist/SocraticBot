import praw

reported_comments = []
def report(comment):
    if comment in reported_comments:
        return
    print "QA violation"
    reported_comments.append(comment)
#    comment.report("QA format violation")
    print comment

def recursive_qa_check(comment, last_type):
    if '?' in str(comment):
        current_type = '?'
    else:
        current_type = '.'

    if last_type == current_type:
        report(comment)

    for c in comment.replies:
        recursive_qa_check(c, current_type)


if __name__ == "__main__":
    r = praw.Reddit('Socrates', '')
    submission = r.get_submission(submission_id='3qmlvv')
    submission.replace_more_comments()
    forest_comments = submission.comments
    for c in forest_comments:
        if '?' in str(c):
            current_type = '?'
            report(c)
        else:
            current_type = '.'
        for r in c.replies:
            recursive_qa_check(r, current_type)

