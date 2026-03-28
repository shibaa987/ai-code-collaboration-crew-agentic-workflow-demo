from crewai.tools import BaseTool
from github import Github
import os
import uuid


class GitHubPRTool(BaseTool):
    name: str = "create_github_pr"
    description: str = (
        "Create a GitHub PR using the provided Python code as file content"
    )

    def _run(self, file_content: str) -> str:
        token = os.getenv("GITHUB_TOKEN")
        repo_name = os.getenv("GITHUB_REPO")

        g = Github(token)
        repo = g.get_repo(repo_name)

        branch_name = f"ai-update-{uuid.uuid4().hex[:6]}"

        # base = repo.get_branch("main")
        base = repo.get_branch("feature/ui")
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base.commit.sha)

        filename = "generated_code.py"

        try:
            contents = repo.get_contents(filename, ref=branch_name)
            repo.update_file(
                contents.path,
                "AI update",
                file_content,
                contents.sha,
                branch=branch_name,
            )
        except:
            repo.create_file(
                filename,
                "AI generated code",
                file_content,
                branch=branch_name,
            )

        pr = repo.create_pull(
            title="AI Generated Code Update",
            body="Automated PR by CrewAI agents",
            head=branch_name,
            base="main",
        )

        return pr.html_url
