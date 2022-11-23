from jinja2 import Template, Environment, FileSystemLoader
import datetime


class ClassConstructor:

    def __init__(self, creator,
                 includes,
                 namespace,
                 base_classes,
                 names,
                 copy_constructor=False,
                 copy_assignment=False,
                 move_constructor=False,
                 move_assignment=False,
                 is_final=False,
                 destructor=False):
        self.creator: str = creator
        self.includes: list(str) = includes
        self.namespace: str = namespace
        self.base_classes: list(str) = base_classes
        self.name: str = ""
        self.names: list(str) = names
        self.copy_constructor: bool = copy_constructor
        self.copy_assignment: bool = copy_assignment
        self.move_constructor: bool = move_constructor
        self.move_assignment: bool = move_assignment
        self.is_final: bool = is_final
        self.destructor: bool = destructor
        self.year: int = datetime.date.today().year

    def __repr__(self):
        return  f'creator:{self.creator},\n' \
                f'includes={self.includes},\n' \
                f'namespace={self.namespace},\n' \
                f'namespace={self.base_classes},\n' \
                f'name={self.name},\n' \
                f'names={self.names},\n' \
                f'copy_constructor={self.copy_constructor},\n' \
                f'copy_assignment={self.copy_assignment},\n' \
                f'move_constructor={self.move_constructor},\n' \
                f'move_assignment={self.move_assignment},\n' \
                f'is_final={self.is_final},\n' \
                f'destructor={self.destructor},\n' \
                f'self.year={self.year}'

    def to_file(self, file_type):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        for name in self.names:
            self.name = name
            template_name = 'template.header.jinja' if file_type == 'h' else 'template.cpp.jinja'
            template = env.get_template(template_name)
            output = template.render(vars(self))
            with open('render/%s.%s' % (name, file_type), 'w') as fh:
                fh.write(output)


if __name__ == "__main__":
    pass
