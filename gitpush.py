from github import Github
g = Github("rohin.hodkasia@amantyatech.com", "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")

repo = g.get_user().get_repo("shellscript")
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open('/home/amantya/PycharmProjects/gitclone/gitpush.py', 'r') as file:
    content = file.read()

# Upload to github
git_prefix = 'folder1/'
git_file = git_prefix + 'gitpush.py'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="main")
    print(git_file + ' CREATED')