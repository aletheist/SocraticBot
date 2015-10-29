from core import get_pairs

class Comment(object):
    def __init__(self, content, replies=None):
        self._content = content
        self.replies = replies or []

    def __str__(self):
        return self._content

    def __repr__(self):
        return "Comment(%s, replies=%s)" % (self._content, self.replies)

    def __hash__(self):
        return hash(self._content)

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self._content == other._content
        return False

class DescribeGetPairs:
    def should_get_pairs(self):
        comment2  = Comment('Comment 2')
        comment1 = Comment('Comment 1', replies=[comment2])
        assert set([(comment1, comment2)]) == set(get_pairs(comment1))

    def should_get_pairs_nested_tree(self):
        comment3 = Comment('Comment 3')
        comment2 = Comment('Comment 2', replies=[comment3])
        comment1 = Comment('Comment 1', replies=[comment2])
        assert set([(comment1, comment2), (comment2, comment3)]) == set(get_pairs(comment1))
