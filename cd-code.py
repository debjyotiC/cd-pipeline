import time
import json
import logging
import github3
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open("configurations/cd-configuration.json") as config_file:
    config = json.load(config_file)

github_config = config["github"]
cd_config = config["cd_details"]

# Authenticate with GitHub
gh = github3.login(token=github_config['token'])

# Initialize the current version
current_version = None


def get_latest_tag(repo):
    """Fetch the latest tag from the repository."""
    try:
        tags = repo.tags()
        latest_tag = next(tags).name
        return latest_tag
    except StopIteration:
        logging.warning("No tags found in the repository.")
        return None


while True:
    try:
        # Get the repository
        repo = gh.repository(owner=github_config['username'], repository=github_config['repository-name'])
        latest_tag = get_latest_tag(repo)

        if latest_tag:
            if current_version is None:
                current_version = latest_tag

            if latest_tag == current_version:
                logging.info("No updates found.")
            else:
                logging.info(f"Update available: {latest_tag}")
                current_version = latest_tag

                compose_command = f"docker compose -f {cd_config['compose_file_path']} up -d"
                os.system(compose_command)

    except github3.exceptions.AuthenticationFailed:
        logging.error("Authentication failed. Please check your GitHub token.")
        break
    except github3.exceptions.GitHubException as e:
        logging.error(f"GitHub error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    # Wait for the specified poll time
    time.sleep(cd_config["poll_time"])
