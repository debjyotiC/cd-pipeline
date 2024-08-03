import time
import json
import logging
import github3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Load configuration
with open("configurations/cd-configuration.json") as f:
    cd_conf = json.load(f)

github_essentials = cd_conf["github"]
cd_essentials = cd_conf["cd_details"]

# Authenticate with GitHub
gh = github3.login(token=github_essentials['token'])

# Initialize the current version
current_version = None

while True:
    try:
        # Get the repository
        repository = gh.repository(owner=github_essentials['username'], repository=github_essentials['repository-name'])

        # Get the latest tag (only fetch the first tag)
        tags = repository.tags()
        current_tag = next(tags).name

        print(current_tag)

        if current_version is None:
            # Set the initial version
            current_version = current_tag

        if current_tag == current_version:
            logging.info("No update")
        else:
            logging.info("Update available")
            # Update the current version
            current_version = current_tag

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Wait for the specified poll time
    time.sleep(cd_essentials["poll_time"])
