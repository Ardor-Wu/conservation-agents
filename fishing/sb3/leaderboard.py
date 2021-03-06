## Note: If a script is edited after it starts running but before the leaderboard
## calculation is performed, it will commit the modified version and not the 
## one that matches the execution.  
## So best to call hash_url early in execution and pass to leaderboard.

from datetime import datetime
from git import Repo
import csv
import os

def hash_url(script):
    ## Commit file and compute GitHub URL
    repo = Repo(".", search_parent_directories=True)
    path = os.path.relpath(script, repo.git.working_dir)
    repo.git.add(path)
    if len(repo.index.diff("HEAD")) > 0:
        repo.git.commit("-m 'robot commit before running script'")
    sha = repo.commit().hexsha
    url = repo.git.remote("get-url", "origin") + "/blob/" + sha + "/" + path
    return url

def leaderboard(agent, env, mean, std, url, file = "results/leaderboard.csv"):
    row_contents = {"agent": agent,
                    "env": env,
                    "mean": mean, 
                    "std": std,
                    "url": url,
                    "date": datetime.now()}
    has_header = os.path.exists(file)                
    with open(file, 'a+') as stream:
        writer = csv.DictWriter(stream, 
                                fieldnames = ["agent", 
                                              "env", 
                                              "mean", 
                                              "std", 
                                              "url", 
                                              "date"])
        if(not has_header):                                      
            writer.writeheader()
        writer.writerow(row_contents)


# leaderboard("X", "B", 3, 0, "leaderboard.py", "test.csv")
