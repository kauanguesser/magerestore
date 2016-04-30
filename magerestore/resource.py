import subprocess


class ResourceManager:
    def __init__(self, resource_config, repo_manager):
        self.resource_config = resource_config
        self.repo_manager = repo_manager
        self.resources = dict()
        self.factory = ResourceFactory(self)

    def get_resource(self, name):
        if name not in self.resources:
            self.resources[name] = self.factory.create(self.resource_config[name])

        return self.resources[name]

    def names(self):
        """Get list of resource names"""
        return sorted([name for name in self.resource_config])


class ResourceFactory:
    def __init__(self, resource_manager):
        self.types = dict()
        self.manager = resource_manager

    def add_type(self, name, type_class):
        self.types[name] = type_class

    def create(self, node):
        node_type = node['type']

        if node_type not in self.types:
            raise KeyError('No resource class defined for node type `{type}`'.format(type=node_type))

        type_class = self.types[node_type]

        return type_class(node, self.manager)


class MagentoDatabaseResource:
    def __init__(self, config, resource_manager):
        self.path = config['path']
        self.manager = resource_manager

    def get_resource(self, progress_callback=None):
        return self.repository.get_file(self.path, progress_callback)

    def import_resource(self):
        args = ['n98-magerun.phar', 'db:import', '--drop', '--compression=gzip', '--drop', '--', self.localpath]
        proc = subprocess.Popen(args)

    def cleanup(self):
        pass
