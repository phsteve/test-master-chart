import yaml
import os


def set_dep_branches(f, branch_requirements):
    y = yaml.load(f)
    for dep in y['dependencies']:
        if dep['name'] in branch_requirements:
            if not branch_requirements[dep['name']]:
                continue
            dep['version'] = dep['version'].replace('any', branch_requirements[dep['name']])
    print(y)
    return y

def write_requirements_yaml(deps):
    with open('requirements.yaml', 'w') as f:
        yaml.dump(deps, f, default_flow_style=False)

def write_values_yaml(branch_requirements):
    values = {}
    for repo in branch_requirements:
        branch = branch_requirements.get(repo)
        if branch:
            values[repo] =  {'commitHash': branch, 'image':{'tag': branch}}
    print(values)
    with open('Values.yaml', 'w') as f:
        yaml.dump(values, f, default_flow_style=False)

if __name__ == '__main__':
    branch_requirements = {
        'kube-toy': os.getenv('CUSTOM_kube_toy'),
        'kube-service': os.getenv('CUSTOM_kube_service')
    }
    with open('requirements.yaml') as f:
        deps = set_dep_branches(f, branch_requirements)
    write_requirements_yaml(deps)
    write_values_yaml(branch_requirements)
