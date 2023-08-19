# Check the quality of a python package

Github action to automatically format files in python packaging. Please ensure github actions has read/write access on a repo before using

Currently supports:

* Auto increment micro version
* Format with black
* Format with isort

This repo has been set-up to enable quickly adding more tasks. See [tasks](package_checker/tasks/) for the current tasks.
When new tasks are added, a workflow will be run on push to update the action.yaml, enabling quick adding of tasks.

This repo uses itself for formatting! See [update-actions.yaml](.github/workflows/update-actions.yaml) to see how to use this repo.
