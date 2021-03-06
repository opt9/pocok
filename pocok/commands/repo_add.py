from .abstract_command import AbstractCommand
from ..services.config_handler import ConfigHandler
from ..services.state import StateHolder
from ..services.state_utils import StateUtils


class RepoAdd(AbstractCommand):

    sub_command = "repo"
    command = ["add", "modify"]
    args = ["<name>", "<git-url>", "[<branch>]", "[<file>]"]
    args_descriptions = {"<name>": "Name of the repository.",
                         "<git-url>": "URL of catalog's GIT repository",
                         "[<branch>]": "Name of the branch that should be checked out.(default: master)",
                         "[<file>]": "Name of the catalog file in the repository (default: pocok-catalog.yml)."}
    description = "Run: 'pocok repo add default https://github.com/shiwaforce/poco-example master' to add new " \
                  "catalog to the config from github and use master branch. Modify command use same metholody."

    def prepare_states(self):
        StateUtils.prepare("catalog_read")

    def resolve_dependencies(self):
        pass

    def execute(self):
        config = dict()
        config['repositoryType'] = 'git'
        config['server'] = StateHolder.args.get('<git-url>')
        if StateHolder.has_args('<branch>'):
            config['branch'] = StateHolder.args.get('<branch>')
        if StateHolder.has_args('<file>'):
            config['file'] = StateHolder.args.get('<file>')
        ConfigHandler.add(new_config=config)


class GitHubAdd(AbstractCommand):

    sub_command = "github"
    command = ["add", "modify"]
    args = ["<name>", "<login>", "[<url>]"]
    args_descriptions = {"<name>": "Name of the repository.",
                         "<login>": "Authentication data for GitHub account. Token or username/password.",
                         "[<url>]": "URL if you want to use your private GitHub server"}
    description = "Run: 'pocok repo add github xxxxxxxx' to add your GitHub account. Afterwards you can list  " \
                  "your GitHub projects in catalog. Modify command use same metholody."

    def prepare_states(self):
        StateUtils.prepare("catalog_read")

    def resolve_dependencies(self):
        pass

    def execute(self):
        config = dict()
        config['repositoryType'] = 'github'
        login = StateHolder.args.get('<login>')
        if "/" in login:
            args = login.split("/")
            config['user'] = args[0]
            config['pass'] = args[1]
        else:
            config['token'] = login
        if StateHolder.has_args('<url>'):
            config['server'] = StateHolder.args.get('<url>')
        ConfigHandler.add(new_config=config)


class GitLabAdd(AbstractCommand):

    sub_command = "gitlab"
    command = ["add", "modify"]
    args = ["<name>", "<login>", "[<url>]", "[<ssh>]"]
    args_descriptions = {"<name>": "Name of the repository.",
                         "<login>": "Authentication data for GitLab account. It works with Token only.",
                         "[<url>]": "URL if you want to use your private GitLab server",
                         "[<ssh>]": "location of SSH key for your GitLab projects (default is '/~/.ssh/id_rsa')"}
    description = "Run: 'pocok repo add gitlab xxxxxxxx' to add your GitLab account. Afterwards you can list  " \
                  "your GitLab projects in catalog. Modify command use same metholody."

    def prepare_states(self):
        StateUtils.prepare("catalog_read")

    def resolve_dependencies(self):
        pass

    def execute(self):
        config = dict()
        config['repositoryType'] = 'gitlab'
        config['token'] = StateHolder.args.get('<login>')
        if StateHolder.has_args('<url>'):
            config['server'] = StateHolder.args.get('<url>')
        if StateHolder.has_args('<ssh>'):
            config['ssh'] = StateHolder.args.get('<ssh>')
        ConfigHandler.add(new_config=config)
