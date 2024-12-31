from github import Github
import os
import git
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# Authenticate with GitHub (use an access token for private repos if necessary)
g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

# Define the repository
repo_name = "alchemyplatform/modular-account"  # replace with "owner/repo" of your target repository
repo = g.get_repo(repo_name)

# Choose the branch or tag you want to extract
# For a branch, use just the branch name, e.g., "main", "dev", "feature-xyz"
# For a tag, use its tag name, e.g., "v1.0.0"
branch_or_tag = "v1.0.0"  # <-- Change this to any branch/tag or tag you wish

# List of common image extensions to skip
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp')

# Recursive function to get files
def get_files(contents, unique_text_file, progress_bar, ref):
    for content_file in contents:
        progress_bar.update(1)  # Increment progress bar for each item processed
        if content_file.type == "dir":
            print(f"Entering directory: {content_file.path}")
            # Recursively get the contents of the directory, specifying the same ref
            subdir_contents = repo.get_contents(content_file.path, ref=ref)
            get_files(subdir_contents, unique_text_file, progress_bar, ref)
        elif content_file.type == "file":
            # Skip image files based on file extension
            if content_file.path.lower().endswith(IMAGE_EXTENSIONS):
                print(f"Skipping image file: {content_file.path}")
                continue

            # Print the file path as a subtitle
            unique_text_file.write(f"\n--- {content_file.path} ---\n\n")
            try:
                if content_file.encoding == "base64":
                    file_content = repo.get_contents(content_file.path, ref=ref).decoded_content.decode("utf-8")
                    unique_text_file.write(file_content + "\n")
                    print(f"Processed file: {content_file.path}")
                else:
                    unique_text_file.write(f"[Skipped unsupported encoding for {content_file.path}]\n")
                    print(f"Skipped file with unsupported encoding: {content_file.path}")
            except UnicodeDecodeError:
                unique_text_file.write(f"[Skipped binary or non-text file: {content_file.path}]\n")
                print(f"Skipped binary or non-text file: {content_file.path}")
        elif content_file.type == "symlink":
            unique_text_file.write(f"\n--- {content_file.path} (Symbolic Link) ---\n")
            unique_text_file.write(f"Target: {content_file.target}\n\n")
            print(f"Processed symbolic link: {content_file.path}")
        elif content_file.type == "submodule":
            unique_text_file.write(f"\n--- {content_file.path} (Submodule) ---\n")
            unique_text_file.write(f"Submodule URL: {content_file.submodule_git_url}\n")
            print(f"Found submodule: {content_file.path}")
            
            # Optional: Clone the submodule repository (requires GitPython)
            try:
                submodule_path = os.path.join("cloned_submodules", content_file.path.replace("/", "_"))
                if not os.path.exists(submodule_path):
                    print(f"Cloning submodule: {content_file.submodule_git_url}")
                    git.Repo.clone_from(content_file.submodule_git_url, submodule_path)
                    unique_text_file.write(f"Submodule cloned to: {submodule_path}\n")
                else:
                    unique_text_file.write(f"Submodule already cloned: {submodule_path}\n")
                    print(f"Submodule already cloned: {submodule_path}")
            except Exception as e:
                unique_text_file.write(f"Failed to clone submodule: {str(e)}\n")
                print(f"Failed to clone submodule: {content_file.path}, Error: {e}")
        else:
            unique_text_file.write(f"\n--- {content_file.path} (Unknown or unsupported content type) ---\n")
            unique_text_file.write("This content type is not supported for direct inclusion.\n")
            print(f"Skipped unknown or unsupported content type: {content_file.path}")

# Open a text file to save all content and initialize progress bar
with open("all_files_combined.txt", "w", encoding="utf-8") as f:
    # Get the top-level contents for the specified branch or tag
    contents = repo.get_contents("", ref=branch_or_tag)
    with tqdm(total=len(contents), desc=f"Processing repository contents ({branch_or_tag})") as progress_bar:
        get_files(contents, f, progress_bar, ref=branch_or_tag)

print("All files and special content have been processed.")
