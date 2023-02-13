from AzureDevops import AzureDevOpsInventory
from AzureDevOpsToCsv import AzureDevOpstoCSV



run = AzureDevOpsInventory()
run.set_project_security_groups()
run.set_project_group_admins()
run.set_pipelines()
run.set_repos() # risk 
run.set_processes()
run.set_agent_pool()
run.set_agent_list()
run.save_json()


to_csv = AzureDevOpstoCSV(run.dir)
to_csv.create_agent_list_csv()
to_csv.create_agent_pools_csv()
to_csv.create_pipelines_csv()
to_csv.create_project_admins_csv()
to_csv.create_projects_csv()
to_csv.create_repos_csv()
