import unittest
from src.main.model.issues import Issues
from src.main.model.issue import Issue
from src.main.model.worklog import Worklog
from src.main.model.worklogs_component import WorklogsForComponent


class TestWorklogsComponent(unittest.TestCase):

    def test_get_usernames_should_return_the_users_that_have_workloads(self):
        # given
        workloads = WorklogsForComponent("component",
                                     [Worklog("id1", "user1", "2021-10-10", 60, "issue1"),
                                          Worklog("id2", "user2", "2021-10-10", 60, "issue2")])

        # when
        usernames = workloads.get_usernames()

        # then
        self.assertEqual(usernames, {"user1", "user2"})

    def test_get_worklogs_for_user_should_return_the_worklogs_for_user(self):
        # given
        workloads = WorklogsForComponent("component",
                                     [Worklog("id1", "user1", "2021-10-10", 60, "issue1"),
                                          Worklog("id2", "user2", "2021-10-10", 60, "issue2")])

        # when
        worklogs_for_user = workloads.get_worklogs_for_user("user1")

        # then
        self.assertEqual(worklogs_for_user.workloads, [Worklog("id1", "user1", "2021-10-10", 60, "issue1")])

    def test_get_worklogs_for_user_should_return_empty_if_user_is_unknown(self):
        # given
        workloads = WorklogsForComponent("component",
                                     [Worklog("id1", "user1", "2021-10-10", 60, "issue1"),
                                          Worklog("id2", "user2", "2021-10-10", 60, "issue2")])

        # when
        worklogs_for_user = workloads.get_worklogs_for_user("user3")

        # then
        self.assertEqual(worklogs_for_user.workloads, [])


if __name__ == "__main__":
    unittest.main()
