from ckanapi import RemoteCKAN

class CkanApi():

    def __init__(self):
        self.instance = RemoteCKAN('https://us-ed-scraping.ckan.io/')

    def get_groups(self):
        groups = self.instance.action.group_list()
        return groups

    def get_organizations(self, all_fields=True):

        organizations = self.instance.action.organization_list(all_fields=all_fields)
        return organizations

    def get_package_list(self):
        packages_names = self.instance.action.package_list()
        return packages_names

