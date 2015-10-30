def get_threads(comment):
    if not comment.replies:
        yield comment,
    for reply in comment.replies:
        if not reply.replies:
            yield comment, reply
        else:
            for r in get_threads(reply):
                yield (comment,) + r
