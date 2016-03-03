try:
    import unittest2 as unittest
except ImportError:
    import unittest
from db_connector import DBConnector, GitHubData, PackageManagerData
from config import Config
from github import GitHub
from package_managers import PackageManagers
from sendgrid_email import SendGrid
import datetime
import os
try:
    basestring
except NameError:
    basestring = str


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_initialization(self):
        github_token = os.environ.get('GITHUB_TOKEN')
        self.assertTrue(isinstance(github_token, basestring))
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        self.assertTrue(isinstance(sendgrid_api_key, basestring))
        mysql_db = os.environ.get('MYSQL_DB')
        self.assertTrue(isinstance(mysql_db, basestring))
        mysql_host = os.environ.get('MYSQL_HOST')
        self.assertTrue(isinstance(mysql_host, basestring))
        mysql_username = os.environ.get('MYSQL_USERNAME')
        self.assertTrue(isinstance(mysql_username, basestring))
        mysql_password = os.environ.get('MYSQL_PASSWORD')
        self.assertTrue(isinstance(mysql_password, basestring))
        mysql_port = os.environ.get('MYSQL_PORT')
        self.assertTrue(isinstance(mysql_port, basestring))
        self.assertTrue(isinstance(self.config.github_user, basestring))
        self.assertTrue(isinstance(self.config.github_repos, list))
        self.assertTrue(isinstance(self.config.package_manager_urls, list))
        self.assertTrue(isinstance(self.config.to_email, basestring))
        self.assertTrue(isinstance(self.config.from_email, basestring))
        self.assertTrue(isinstance(self.config.email_subject, basestring))
        self.assertTrue(isinstance(self.config.email_body, basestring))


class TestDBConnector(unittest.TestCase):
    def setUp(self):
        self.db = DBConnector()

    def test_add_and_delete_data(self):
        github_data_import = GitHubData(
                                date_updated=datetime.datetime.now(),
                                language='repo_name',
                                pull_requests=0,
                                open_issues=0,
                                number_of_commits=0,
                                number_of_branches=0,
                                number_of_releases=0,
                                number_of_contributors=0,
                                number_of_watchers=0,
                                number_of_stargazers=0,
                                number_of_forks=0
                                )
        res = self.db.add_data(github_data_import)
        self.assertTrue(isinstance(res, GitHubData))
        res = self.db.delete_data(res.id, 'github_data')
        self.assertTrue(res)

        packagedata = PackageManagerData(
                                date_updated=datetime.datetime.now(),
                                csharp_downloads=0,
                                nodejs_downloads=0,
                                php_downloads=0,
                                python_downloads=0,
                                ruby_downloads=0
                                )
        res = self.db.add_data(packagedata)
        self.assertTrue(isinstance(res, PackageManagerData))
        res = self.db.delete_data(res.id, 'package_manager_data')
        self.assertTrue(res)

    def test_get_data(self):
        github_data = self.db.get_data(GitHubData)
        self.assertTrue(isinstance(github_data, list))
        self.assertTrue(isinstance(github_data[0], GitHubData))


class TestGitHub(unittest.TestCase):
    def setUp(self):
        self.github = GitHub()
        self.db = DBConnector()
        self.config = Config()

    def test_update_library_data(self):
        res = self.github.update_library_data(self.config.github_user,
                                              self.config.github_repos[0])
        self.assertTrue(isinstance(res, GitHubData))
        res = self.db.delete_data(res.id, 'github_data')
        self.assertTrue(res)


class TestPackageManagers(unittest.TestCase):
    def setUp(self):
        self.pm = PackageManagers()
        self.db = DBConnector()
        self.config = Config()

    def test_update_package_manager_data(self):
        res = self.pm.update_package_manager_data(
               self.config.package_manager_urls)
        self.assertTrue(isinstance(res, PackageManagerData))
        res = self.db.delete_data(res.id, 'package_manager_data')
        self.assertTrue(res)


class TestSendGridEmail(unittest.TestCase):
    def setUp(self):
        self.sg = SendGrid()
        self.config = Config()

    def test_send_email(self):
        res = self.sg.send_email(
               'elmer.thomas+test@sendgrid.com',
               self.config.from_email,
               self.config.email_subject,
               self.config.email_body
               )
        self.assertEqual(200, res[0])
        self.assertEqual('{"message":"success"}', res[1].decode("utf-8"))

if __name__ == '__main__':
    unittest.main()