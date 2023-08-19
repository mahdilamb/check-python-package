
import json
from package_checker import api


def github_model_test():
    json_string = """{
		"token": "***",
		"job": "prepare",
		"ref": "refs/heads/add-github-json",
		"sha": "13cb54bee3ada7341d5f889d999632f4872a02e9",
		"repository": "mahdilamb/check-python-package",
		"repository_owner": "mahdilamb",
		"repository_owner_id": "4696915",
		"repositoryUrl": "git://github.com/mahdilamb/check-python-package.git",
		"run_id": "5910476949",
		"run_number": "31",
		"retention_days": "90",
		"run_attempt": "1",
		"artifact_cache_size_limit": "10",
		"repository_visibility": "public",
		"repo-self-hosted-runners-disabled": false,
		"enterprise-managed-business-id": "",
		"repository_id": "680058993",
		"actor_id": "4696915",
		"actor": "mahdilamb",
		"triggering_actor": "mahdilamb",
		"workflow": "Check code quality and run unit tests",
		"head_ref": "",
		"base_ref": "",
		"event_name": "push",
		"event": {
			"after": "13cb54bee3ada7341d5f889d999632f4872a02e9",
			"base_ref": null,
			"before": "f7546e38e472c0bdf81b2e1f05a354cec4d1dbd0",
			"commits": [{
					"author": {
						"email": "mahdilamb@gmail.com",
						"name": "Mahdi Lamb",
						"username": "mahdilamb"
					},
					"committer": {
						"avatar_url": "https://avatars.githubusercontent.com/u/4696915?v=4",
						"events_url": "https://api.github.com/users/mahdilamb/events{/privacy}",
						"followers_url": "https://api.github.com/users/mahdilamb/followers",
						"following_url": "https://api.github.com/users/mahdilamb/following{/other_user}",
						"gists_url": "https://api.github.com/users/mahdilamb/gists{/gist_id}",
						"gravatar_id": "",
						"html_url": "https://github.com/mahdilamb",
						"id": 4696915,
						"login": "mahdilamb",
						"node_id": "MDQ6VXNlcjQ2OTY5MTU=",
						"organizations_url": "https://api.github.com/users/mahdilamb/orgs",
						"received_events_url": "https://api.github.com/users/mahdilamb/received_events",
						"repos_url": "https://api.github.com/users/mahdilamb/repos",
						"site_admin": false,
						"starred_url": "https://api.github.com/users/mahdilamb/starred{/owner}{/repo}",
						"subscriptions_url": "https://api.github.com/users/mahdilamb/subscriptions",
						"type": "User",
						"url": "https://api.github.com/users/mahdilamb"
					}
				},
				"server_url": "https://github.com",
				"api_url": "https://api.github.com",
				"graphql_url": "https://api.github.com/graphql",
				"ref_name": "add-github-json",
				"ref_protected": false,
				"ref_type": "branch",
				"secret_source": "Actions",
				"workflow_ref": "mahdilamb/check-python-package/.github/workflows/update-actions.yaml@refs/heads/add-github-json",
				"workflow_sha": "13cb54bee3ada7341d5f889d999632f4872a02e9",
				"workspace": "/home/runner/work/check-python-package/check-python-package",
				"action": "__mahdilamb_check-python-package",
				"event_path": "/home/runner/work/_temp/_github_workflow/event.json",
				"action_repository": "",
				"action_ref": "",
				"path": "/home/runner/work/_temp/_runner_file_commands/add_path_8da3e633-853a-4937-9e0a-8a7d0aaf5ce7",
				"env": "/home/runner/work/_temp/_runner_file_commands/set_env_8da3e633-853a-4937-9e0a-8a7d0aaf5ce7",
				"step_summary": "/home/runner/work/_temp/_runner_file_commands/step_summary_8da3e633-853a-4937-9e0a-8a7d0aaf5ce7",
				"state": "/home/runner/work/_temp/_runner_file_commands/save_state_8da3e633-853a-4937-9e0a-8a7d0aaf5ce7",
				"output": "/home/runner/work/_temp/_runner_file_commands/set_output_8da3e633-853a-4937-9e0a-8a7d0aaf5ce7",
				"action_path": "/home/runner/work/_actions/mahdilamb/check-python-package/add-github-json",
				"action_status": "success",
			}"""
    print(api.Github.model_validate(json.loads(json_string)))
if __name__=="__main__":
    import sys,pytest
    sys.exit(pytest.main(["-v", "-s"]+sys.argv))
