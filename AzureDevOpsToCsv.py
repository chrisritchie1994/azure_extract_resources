import pandas as pd
import json 

class AzureDevOpstoCSV:
    def __init__(self, dir):
        self.dir = dir
        if not dir:
            self.dir = ''

        
    def create_project_admins_csv(self):
        resource_type = "project_admins"
        with open(f"{self.dir}/{resource_type}.json") as f:
            project_admins = json.load(f)
        
        project_admin_list = []
        for project, value in project_admins.items():
            for k, v in value.items():
                project_admin_list.append({"project": project, 
                                           "displayName": v['displayName'],
                                           "mailAddress": v['mailAddress'],
                                           'principalName': v['principalName'],
                                           'directoryAlias': v['directoryAlias']
                                           })
        
        df = pd.DataFrame(project_admin_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")

    def create_repos_csv(self):
        resource_type = "repos"
        with open(f"{self.dir}/{resource_type}.json") as f:
            repos = json.load(f)
        repo_list = []

        for project, value in repos.items():
            for v in value:
                repo_list.append({"project": project, 
                                    "name": v['name'],
                                    "remote_url": v['remoteUrl'],
                                    "web_url": v['webUrl'],
                                    "size": v['size']
                                })
                
        df = pd.DataFrame(repo_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")


    def create_projects_csv(self):
        resource_type = "projects"
        with open(f"{self.dir}/{resource_type}.json") as f:
            projects = json.load(f)
        projects_list = []

        for dict in projects['value']:
            projects_list.append(dict)
                    
        df = pd.DataFrame(projects_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")


    def create_pipelines_csv(self):
        resource_type = "pipelines"
        with open(f"{self.dir}/{resource_type}.json") as f:
            pipelines = json.load(f)
        pipelines_list = []

        for project, value in pipelines.items():
            for v in value:
                if v:
                    append_dict = {"project": project, 
                                    "authoredBy": v['authoredBy']["uniqueName"],
                                    "createdDate": v['createdDate'],
                                    "latestBuild": v['latestBuild'],
                                    "name": v['name'],
                                    "path": v['path'], 
                                    "type": v['type']}
                    
                    pipelines_list.append(append_dict)
                
        df = pd.DataFrame(pipelines_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")

    def create_agent_pools_csv(self):
        resource_type = "agent_pool"
        with open(f"{self.dir}/{resource_type}.json") as f:
            agent_pool = json.load(f)
        agent_pool_list = []

        for record in agent_pool:
            record['createdBy'] = record['createdBy']['uniqueName']
            record['owner'] = record['owner']['uniqueName']
            agent_pool_list.append(record)

        df = pd.DataFrame(agent_pool_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")

    def create_agent_list_csv(self):
        resource_type = "agent_list"
        with open(f"{self.dir}/{resource_type}.json") as f:
            agents = json.load(f)
        agent_list = []

        for pool_id, v in agents.items():
            if v:
                for agent in v:
                    agent['pool_id'] = pool_id
                    agent['authorization'] = None

                    agent_list.append(agent)
                    
        df = pd.DataFrame(agent_list)
        df.to_csv(f"{self.dir}/{resource_type}.csv")

            

