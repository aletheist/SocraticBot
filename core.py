def get_pairs(root):
    for reply in root.replies:
        if reply.replies:
            for pair in get_pairs(reply):
                yield pair
        yield root, reply
