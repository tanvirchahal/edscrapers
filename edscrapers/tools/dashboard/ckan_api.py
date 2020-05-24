from ckanapi import RemoteCKAN

class CkanApi():

    def __init__(self):
        self.instance = RemoteCKAN('https://us-ed-scraping.ckan.io/')

    def get_groups(self):
        groups = self.instance.action.group_list()
        return groups

    def get_organizations_data(self, all_fields=True):

        organizations = self.instance.action.organization_list(all_fields=all_fields)

        organization_list = []
        for organization in organizations:
            count = organization.get("package_count", 0)
            name = organization.get("name", "")
            organization_list.append({name : count})

        return organization_list

    def get_package_list(self):
        packages_names = self.instance.action.package_list()
        return packages_names

    def get_total_number_scraped_packages(self):
        result = self.instance.action.package_search(fq='scraped_from:*')
        return result.get("count", 0)

