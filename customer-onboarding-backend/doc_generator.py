"""Documentation generator from DocStrings present within the code."""
import configparser
import os
import shutil
from typing import Any, Dict, List

from pexpect.run import run


def get_config_dir_path(connector: str, config_dir_name: str) -> str:
    """Get configurations directory path.

    :param connector: Name of the connector
    :type connector: str
    :param config_dir_name: Configurations directory name
    :type config_dir_name: str
    :return: Configuratins directory path
    :rtype: str
    """
    config_dir: str = ""
    cwd = os.getcwd()
    cwd_list = [item.lower() for item in cwd.split(os.sep)]
    name: str = connector.replace(" ", "_").lower()
    if name == cwd_list[-1]:
        # Current working directory is the connector directory
        config_dir = os.path.join(cwd, config_dir_name)
    elif name in cwd_list:
        # Current working directiory is in connector directory
        index = cwd_list.index(name)
        cwd = f"{os.sep}".join(cwd_list[:index + 1])
        config_dir = os.path.join(cwd, config_dir_name)
    else:
        # Current working directory may have conenctor directory
        for _, dirs, _ in os.walk(cwd):
            if name in [item.lower() for item in dirs]:
                config_dir = os.path.join(cwd, name, config_dir_name)
                break

    return config_dir


def read_config(filepath: str) -> Any:
    """Read the documentation generator configurations.

    :param filepath: Configurations directory path
    :type filepath: str
    :return: Connectors structural configurations
    :rtype: Any
    """
    config = configparser.ConfigParser()
    config.read(filepath)
    return config['STRUCTURE']


def create_docs(project_dir: str) -> str:
    """Create docs directory.

    if the directory already exists, it will delete it and create an empty one.

    :param project_dir: Present working directory
    :type project_dir: str
    :return: Documentation directory path
    :rtype: str
    """
    docs_path = os.path.join(project_dir, 'docs')
    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)
    os.mkdir(docs_path)

    return docs_path


def run_sphinx(config: Dict[str, Any]) -> None:
    """Run the sphinx command.

    :param config: Configurations required for sphinx
    :type config: Dict[str, Any]
    """
    events = {
        r'> Separate source and build directories \(y\/n\) \[n\]\:': 'n\n',
        '> Project name:': config['NAME'] + '\n',
        r'> Author name\(s\):': config['AUTHOR'] + '\n',
        r'> Project release \[]:': config['VERSION'] + '\n',
        r'> Project language \[en]:': 'en\n'
    }
    # Call sphinx-quickstart
    run('sphinx-quickstart', events=events)


def set_doc_config() -> None:
    """Set documentation configurations."""
    # Read the config file inside the docs folder.
    config_path = os.path.join("conf.py")
    with open(config_path, "r") as conf_file:
        contents = conf_file.readlines()

    # Include root path of the project
    contents.insert(16, 'import os\n')
    contents.insert(17, 'import sys\n')
    contents.insert(18, 'sys.path.insert(0, os.path.abspath("../src/"))\n')
    for index, content in enumerate(contents):
        if "extensions = [" in content:
            if contents[index + 1] == "]\n":
                contents.pop(index + 1)
            contents.pop(index)
            contents.insert(index, "extensions = ['sphinxcontrib.fulltoc', 'sphinx.ext.autodoc', 'pallets_sphinx_themes']\n")

    # Write the config content to file.
    with open(config_path, "w") as conf_file:
        conf_file.writelines("".join(contents))


def update_index_rst(project_path: str, config: Dict[str, Any]) -> None:
    """Update index.rst file.

    :param project_path: Project directory path
    :type project_path: str
    :param config: Configurations
    :type config: Dict[str, Any]
    """
    index_path = os.path.join("index.rst")
    # Read the index.rst file present inside docs
    with open(index_path, "r") as index_file:
        contents = index_file.readlines()

    # Remove heading and styling line from index.rst
    contents.pop(5)
    contents.pop(5)

    # Include README file and name modules to index.rst
    readme_path = os.path.join(project_path, "README.md")
    os.system(f'm2r {readme_path}')  # nosec

    readme_rst = "README.rst"
    contents.insert(5, f'.. include:: {readme_rst}\n')
    contents.insert(12, '   modules')

    # Write Index content to file
    with open(index_path, "w") as index_file:
        index_file.writelines("".join(contents))

    # Move REAME.rst to source directory
    src_readme = os.path.join(project_path, readme_rst)
    dst_readme = os.path.join(project_path, "docs", readme_rst)
    os.popen(f'cp {src_readme} {dst_readme}')  # nosec

    # Create .rst files for module
    module_path = os.path.join(project_path, config['PACKAGE'])
    run('sphinx-apidoc --module-first -M -o  . {module_path}'.format(module_path=module_path))

    # Create html files for the module
    run('make html')

    with open(index_path, "r") as index_file:
        contents = index_file.readlines()

    # Remove name modules from index.rst and project name
    contents.pop(12)
    source = config['PACKAGE'].split('/')[-1]
    contents.insert(11, f'\n   {source}\n')

    with open(index_path, "w") as index_file:
        index_file.writelines("".join(contents))


def get_rst_filename(package: str, root: str):
    """Get the rst filename.

    :param package: Package name
    :type package: str
    :param root: Root package name
    :type root: str
    """
    rst_filename: str = ""
    if root == package:
        rst_filename = f"{package}.rst"
    else:
        rst_filename = f"{root}.{package}.rst"
    return rst_filename


def remove_heading(config: Dict[str, Any]) -> None:
    """Remove unused headings and sub headings.

    :param config: Configurations
    :type config: Dict[str, Any]
    """
    rst_filename: str = ""
    sub_package_list = config['SUB_PACKAGES'].split(",")
    for sub_package in sub_package_list:
        rst_filename = get_rst_filename(sub_package, sub_package_list[0])

        contents = []
        if os.path.exists(rst_filename):
            with open(rst_filename, "r") as rst_file:
                contents = rst_file.readlines()

            contents.pop(0)
            contents.pop(7)
            contents.pop(7)

        # Remove Submodules from the rst file
        sub_modules = 'Submodules\n'
        if sub_modules in contents:
            sub_index = contents.index(sub_modules)
            contents.remove(sub_modules)
            contents.pop(sub_index)

        # Remove line ending with module from rst file
        for modules in contents:
            if modules.strip().endswith("module"):
                index = contents.index(modules)
                contents.pop(index)
                contents.pop(index)

        with open(rst_filename, "w") as rst_file:
            rst_file.writelines("".join(contents))


def update_content_with_automodule(contents: List[str], sub_modules: List[str], count: int) -> List[str]:
    """Update contents with automodule.

    :param contents: Contents to be updated
    :type contents: List[str]
    :param sub_modules: Submodules
    :type sub_modules: List[str]
    :param count: Count of lines
    :type count: int
    :return: Updated contents. list
    :rtype: List[str]
    """
    for modules in contents[6:]:
        if modules.startswith('.. automodule::'):
            index = contents.index(modules)
            contents.insert(index, f"{sub_modules[count]}\n")
            contents.insert(index + 1, '--------------------------\n')
            count += 1
    return contents


def add_headings(config: Dict[str, Any]) -> None:
    """Add new headings and subheadings.

    :param config: Configurations
    :type config: Dict[str, Any]
    :raises IndexError: Missing module
    """
    rst_filename: str = ""
    sub_package_list = config['SUB_PACKAGES'].split(",")
    for sub_package in sub_package_list:
        rst_filename = get_rst_filename(sub_package, sub_package_list[0])

        with open(rst_filename, "r") as rst_file:
            contents = rst_file.readlines()
            contents.insert(0, f'{sub_package}\n')

        sub_modules = config[sub_package.upper()].split(",")
        count = 0
        while count < len(sub_modules):
            if sub_package_list[0] == sub_package:
                contents = update_content_with_automodule(contents, sub_modules, count)
                contents.pop(0)
                contents.pop(0)
            else:
                try:
                    contents = update_content_with_automodule(contents, sub_modules, count)
                except IndexError as err:
                    raise IndexError('Check the configurations for missing module or package') from err

            with open(rst_filename, "w") as rst_file:
                rst_file.writelines("".join(contents))

            if count < 1:
                break


def generate_documentation(project_name: str, config_dirname: str, config_filename: str) -> None:
    """Generate source code documentation.

    :param project_name: Name of the project
    :type project_name: str
    :param config_dirname: configurations directory name
    :type config_dirname: str
    """
    # Get the configurations directory path.
    config_dir = get_config_dir_path(project_name, config_dirname)

    # read connector documentation configurations
    filepath = os.path.join(config_dir, config_filename)
    print(f"Reading configurations from {filepath}")
    config = read_config(filepath)

    # Project directory path
    project_dir = os.path.dirname(config_dir)

    # Create docs directory if it does not exists.
    print("Cleaning docs directory.")
    docs_path = create_docs(project_dir)

    # Change directory to doccumentation directory
    print(f"Changing current directory to '{docs_path}'")
    os.chdir(docs_path)

    # Run sphinx
    print("Running sphinx to generate dcumentation.")
    run_sphinx(config)

    # Set the configurations for documentation.
    print("Updating documentation configurations in `conf.py` file.")
    set_doc_config()

    # Update index.rst
    print("Updating `index.rst` file.")
    update_index_rst(project_dir, config)

    print("Updating headings for more readability.")
    # Remove not needed headings
    remove_heading(config)
    # Add/update headings.
    add_headings(config)

    # clean using make
    print("Cleaning the build.")
    os.system('make clean')  # nosec

    # Delete modules.rst file
    modules_rst = os.path.join(docs_path, "modules.rst")
    if modules_rst:
        os.remove(modules_rst)

    # Remove README.rst if it exists.
    readme_rst = os.path.join(project_dir, "README.rst")
    if os.path.exists(readme_rst):
        print(f"Deleting unused '{readme_rst}' file.")
        os.remove(readme_rst)

    # Create the html after the changes
    print("Generating html documentation from docstrings.")
    os.system('make html')  # nosec


if __name__ == '__main__':
    generate_documentation("PyLog", "config", "documentation.cfg")