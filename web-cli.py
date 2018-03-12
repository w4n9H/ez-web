# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json
import shutil


ez_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def load_json_file(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp, encoding='utf-8')


def check_django():
    try:
        import django
        v = django.VERSION
        if v[0] != 1 and v[1] < 11:
            raise Exception('django version < 1.11')
        return '.'.join([str(i) for i in list(v)])
    except Exception as error:
        raise Exception('{}'.format(error))


def create_django_project_or_app(name, path, operation_type):  # project_name, project_root_path
    # create_django_project_or_app('test_project', '/Users/wangyazhe/Code/github', 'startproject')
    # create_django_project_or_app('test_app', '/Users/wangyazhe/Code/github/test_project', 'startapp')
    from django.core.management import execute_from_command_line
    project_path = os.path.join(path, name)
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    argv_list = ['django-admin', operation_type, name, project_path]
    execute_from_command_line(argv_list)


def create_module_dir(project_path, module_list, module_type):
    # create utils dir
    ez_module_dir = os.path.join(ez_path, module_type)
    project_module_dir = os.path.join(project_path, module_type)
    if not os.path.exists(project_module_dir):
        os.mkdir(project_module_dir)
    # move utils
    for module in module_list:
        module_name = module.get('name', '')
        module_version = module.get('version', '')
        module_py_name = '{}_{}_{}.py'.format(module_type, module_name, module_version)

        ez_module_path = os.path.join(ez_module_dir, module_py_name)
        if os.path.exists(ez_module_path):
            move_name = '{}_{}.py'.format(module_type, module_name)
            project_module_path = os.path.join(project_module_dir, move_name)
            print ez_module_path
            shutil.copy(ez_module_path, project_module_path)


def create_apps_module(project_path, apps_list):
    # create apps dir
    ez_apps_dir = os.path.join(ez_path, 'apps')
    project_apps_dir = os.path.join(project_path, 'apps')
    if not os.path.exists(project_apps_dir):
        os.mkdir(project_apps_dir)
    # move and create apps
    for apps in apps_list:
        apps_name = apps.get('name', None)
        apps_version = apps.get('version', None)

        if apps_version:
            ez_app_dir = os.path.join(ez_apps_dir, '{}_{}'.format(apps_name, apps_version))
            if os.path.exists(ez_app_dir):
                project_app_dir = os.path.join(project_apps_dir, apps_name)
                shutil.copytree(ez_app_dir, project_app_dir)
        else:
            create_django_project_or_app(apps_name, project_apps_dir, 'startapp')


def create_project():
    project_config = load_json_file('package.json')
    root_path = project_config.get('path', None)
    project_name = project_config.get('name', None)
    project_type = project_config.get('type', None)

    django_version = check_django()
    print django_version

    if project_name and root_path and project_type:
        utils_list = project_config.get('utils', [])
        print project_name, root_path, project_type
        if project_type == 'django':
            apps_list = project_config.get('apps', [])
            middleware_list = project_config.get('middleware', [])
            project_path = os.path.join(root_path, project_name)
            create_django_project_or_app(project_name, root_path, 'startproject')
            if utils_list:
                create_module_dir(project_path, utils_list, 'utils')
            if apps_list:
                create_apps_module(project_path, apps_list)
            if middleware_list:
                create_module_dir(project_path, middleware_list, 'middleware')
        elif project_type == 'flask':
            pass
        elif project_type == 'tornado':
            pass
        else:
            raise
    else:
        raise Exception()


def main():
    pass


if __name__ == '__main__':
    create_project()
    # print load_json_file('package.json')
    # create_django_project_or_app('test_project', '/Users/wangyazhe/Code/github', 'startproject')
    # create_django_project_or_app('test_app', '/Users/wangyazhe/Code/github/test_project', 'startapp')
    # print check_django()

