from socrates import get_threads, find_potential_violations

from hypothesis import strategies, Settings, Verbosity
from hypothesis import given

class Comment(object):
    def __init__(self, content, replies=None):
        self._content = content
        self.replies = replies or []

    def __str__(self):
        return self._content

    def __repr__(self):
        return "C(%s)" % self._content

    def __hash__(self):
        return hash(self._content)

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self._content == other._content
        return False

class DescribeGetThreads:
    def should_get_simple_thread(self):
        comment1 = Comment('Comment 1')
        assert [[comment1]] == list(get_threads(comment1))

    def should_get_two_thread(self):
        comment2 = Comment('Comment 2')
        comment1 = Comment('Comment 1', replies=[comment2])
        assert [[comment1, comment2]] == list(get_threads(comment1))

    def should_get_multiple_children(self):
        comment3 = Comment('Comment 3')
        comment2 = Comment('Comment 2')
        comment1 = Comment('Comment 1', replies=[comment2, comment3])
        assert [[comment1, comment2], [comment1, comment3]] == list(get_threads(comment1))

    def should_get_three_thread(self):
        comment3 = Comment('Comment 3')
        comment2 = Comment('Comment 2', replies=[comment3])
        comment1 = Comment('Comment 1', replies=[comment2])
        assert [[comment1, comment2, comment3]] == list(get_threads(comment1))

    def should_get_two_threads_different_length(self):
        comment4 = Comment('Comment 4')
        comment3 = Comment('Comment 3', replies=[comment4])
        comment2 = Comment('Comment 2')
        comment1 = Comment('Comment 1', replies=[comment2, comment3])
        assert [[comment1, comment2], [comment1, comment3, comment4]] == list(get_threads(comment1))

class CheckFindPotentialViolations:
    def check_uneven_number_of_questions(self):
        branch = ['answer', 'question?', 'bad question?']
        results = set(find_potential_violations(branch))
        assert 'bad question?' in results
