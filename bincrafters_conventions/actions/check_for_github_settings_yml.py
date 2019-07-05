import os


def check_for_github_settings_yml(main):
    """  Check if the repo contains a .github/settings.yml file
    :param main: Output stream
    """
    github_settings = os.path.join(".github", "settings.yml")
    if os.path.isfile(github_settings):
        main.output_result_check(passed=True, title="'{}' file found".format(github_settings))
        return True
    main.output_result_check(passed=False, title=".github/settings.yml",
                             reason="could not be found. Please check out https://github.com/bincrafters/conan-templates/blob/master/.github/settings.yml")
    return False
