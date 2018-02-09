import os
from .file_repository import FileRepository
from .git_repository import GitRepository
from .svn_repository import SvnRepository
from .state import StateHolder
from .console_logger import *


class ProjectUtils:

    @staticmethod
    def get_project_repository(project_element, ssh):
        """Get and store repository handler for named project"""
        if StateHolder.offline:
            repo_handler = FileRepository(target_dir=ProjectUtils.get_target_dir(project_element=project_element))
        elif 'git' in project_element:
            branch = project_element.get('branch', 'master')
            repo_handler = GitRepository(target_dir=ProjectUtils.get_target_dir(project_element=project_element),
                                         url=project_element.get('git'), branch=branch,
                                         git_ssh_identity_file=ssh)
        elif 'svn' in project_element:
            repo_handler = SvnRepository(target_dir=ProjectUtils.get_target_dir(project_element=project_element),
                                         url=project_element.get('svn'))
        else:
            repo_handler = FileRepository(target_dir=ProjectUtils.get_target_dir(project_element=project_element))
        StateHolder.repositories[StateHolder.name] = repo_handler
        return repo_handler

    @staticmethod
    def add_repository(target_dir):

        repo_handler = FileRepository(target_dir=target_dir)
        StateHolder.repositories[StateHolder.name] = repo_handler
        return repo_handler

    @staticmethod
    def get_compose_file(project_element, ssh, silent=False):
        """Get compose file from project repository """

        if StateHolder.config is None:
            repository = ProjectUtils.add_repository(target_dir=StateHolder.work_dir)
            # TODO
            file = repository.get_file('pocok.yml')
        else:
            repo_handler = ProjectUtils.get_project_repository(project_element=project_element, ssh=ssh)
            # TODO
            file = repo_handler.get_file(project_element.get('file', 'pocok.yml'))
        if not os.path.exists(file):
            if silent:
                return None
            ColorPrint.exit_after_print_messages(
                message="Compose file : %s not exists in project : %s " % (str(file), str(StateHolder.name)),
                doc=Doc.POCOK_CATALOG)
        return file

    @staticmethod
    def get_file(file):
        """Get file from project repository"""
        return StateHolder.repositories.get(StateHolder.name).get_file(file)

    @staticmethod
    def get_target_dir(project_element):
        return os.path.join(StateHolder.work_dir, project_element.get('repository_dir', StateHolder.name))

    @staticmethod
    def get_list_value(value):
        """Get list format, doesn't matter the config use one or list plan"""
        lst = list()
        if type(value) is list:
            lst.extend(value)
        else:
            lst.append(value)
        return lst

