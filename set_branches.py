import yaml
import os

branch_requirements = {
    'kube-toy': os.getenv('CUSTOM_kube_toy'),
    'kube-service': os.getenv('CUSTOM_kube_service')
}

def set_dep_branches(f):
    y = yaml.load(f)
    for dep in y['dependencies']:
        if dep['name'] in branch_requirements:
            if not branch_requirements[dep['name']]:
                continue
            dep['version'] = dep['version'].replace('any', branch_requirements[dep['name']])
    return y

def write_yaml(deps):
    with open('requirements.yaml', 'w') as f:
        yaml.dump(deps, f, default_flow_style=False)

if __name__ == '__main__':
    with open('requirements.yaml') as f:
        deps = set_dep_branches(f)
    with open('requirements.yaml', 'w') as f:
        write_yaml(deps)
