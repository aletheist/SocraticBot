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
