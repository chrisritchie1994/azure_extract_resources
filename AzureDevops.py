from Config import Config
import requests
import json
import base64
from datetime import datetime
import os
import subprocess

class AzureDevOpsInventory:
    def __init__(self) -> None:
        self.config = Config()
        self.projects = None
        self.set_projects()
        self.project_list = None
        self.set_project_list()
        self.project_admins = None
        self.project_security_groups = None
        self.pipelines = None
        self.repos = None
        self.processes = None
        self.agent_pool = None
        self.agent_list = None
        self.resources = ['projects', 'project_admins', 'project_security_groups', "pipelines", "repos", "processes", "agent_pool", "agent_list"]
        self.date_time = self.set_time()
        self.dir = f'{self.config.org_base}-{self.date_time}'
        self.create_folder_if_not_exists()

    def set_project_list(self):
        project_list = []
        for project in self.projects["value"]:
            project_list.append(project["name"])
        self.project_list = project_list
            
    def set_time(self):
        now = datetime.now()
        time_and_day = now.strftime("%Y-%m-%d %H H")
        return time_and_day
    
    def pull_response(self, resource_target):
        auth = base64.b64encode(f"{self.config.username}:{self.config.pat}".encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {auth}"
        }

        url = self.config.org_url + resource_target
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # If successful, parse the response as JSON
            dict_payload = json.loads(response.content)

            return dict_payload
        
        else:
            # If the request was not successful, print an error message
            print(f"Failed to retrieve payload with status code {response.status_code}")
            return None
        

    def pull_from_azure_cli(self, core_cmd):
        mandatory_cmd = f"az devops logout & echo {self.config.pat} | az devops login --organization={self.config.org_url} & "
        cmd = mandatory_cmd + core_cmd
        ret = subprocess.run(cmd, capture_output=True, shell=True)

        dict_output = json.loads(ret.stdout.decode().replace("Logged out of all Azure DevOps organizations.", ""))

        return dict_output

    def set_projects(self):
        payload = self.pull_response("/_apis/projects?api-version=6.1")
        self.projects = payload

    def set_processes(self):
        payload = self.pull_response("/_apis/process/processes?api-version=7.0")
        self.processes = payload

    def set_project_security_groups(self):
        project_security_groups = {}
        for project in self.projects["value"]: 
            project_security_groups[project['name']] = self.pull_from_azure_cli(f"az devops security group list --organization={self.config.org_url} --project=\"{project['name']}\"")
        self.project_security_groups = project_security_groups

    def set_project_group_admins(self):
        project_admins = {}
        for project, value in self.project_security_groups.items():
            graph_groups = value['graphGroups']
            for group in graph_groups:
                if group["displayName"] == "Project Administrators":
                    project_admins[project] = self.pull_from_azure_cli(f"az devops security group membership list --id={group['descriptor']} --organization={self.config.org_url}")
        self.project_admins = project_admins

    def set_pipelines(self):
        pipelines = {}
        for project in self.project_list:
            pipelines[project] = self.pull_from_azure_cli(f"az pipelines list --project=\"{project}\" --organization={self.config.org_url}")
        self.pipelines = pipelines

    def set_repos(self):
        repos = {}
        for project in self.project_list :
            repos[project] = self.pull_from_azure_cli(f"az repos list --project=\"{project}\" --organization={self.config.org_url}")
        self.repos = repos

    def set_agent_pool(self):
        self.agent_pool = self.pull_from_azure_cli(f"az pipelines pool list --organization={self.config.org_url}")

    def set_agent_list(self):
        agent_dict = {}
        for agent_pool in self.agent_pool:
            agent_dict[agent_pool["id"]] = self.pull_from_azure_cli(f"az pipelines agent list --organization={self.config.org_url} --pool-id={agent_pool['id']}")
        self.agent_list = agent_dict

    def dump_json_into_file(self, resource_type, data):
        path = f"{self.config.org_base}-{self.date_time}\{resource_type}.json"
        with open(path, 'w') as file:
            json.dump(data, file)

    def save_json(self):

        for resource in self.resources:
            self.dump_json_into_file(resource, self.__getattribute__(resource))

    def create_folder_if_not_exists(self):
        if not os.path.exists(f"{self.config.org_base}-{self.date_time}"):
            os.makedirs(f"{self.config.org_base}-{self.date_time}")