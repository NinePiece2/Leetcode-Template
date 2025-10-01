# Leetcode Solutions

## Table Of Contents
- [Leetcode Solutions](#leetcode-solutions)
  - [Table Of Contents](#table-of-contents)
  - [Description](#description)
    - [Usage Steps](#usage-steps)
    - [Workflow Steps](#workflow-steps)
  - [My Leetcode Stats](#my-leetcode-stats)
  - [Table of my Solutions](#table-of-my-solutions)

<br/>
<p align="center">
  <a href="https://leetcode.romitsagu.com/">
    <img src="https://img.shields.io/badge/Site%20Link-Click%20Here-blue?style=for-the-badge&logo=vercel" alt="Open App"/>
  </a>
</p>

## Description

This is a repo to store my leetcode solutions but I went a bit Schizo with it and it pulls the leetcode solutions, creates READMEs with the problema and solution and then converts it into an Mkdocs website hosted on GitHub Pages.

Working demo [here](https://github.com/NinePiece2/Leetcode)

### Usage Steps
1. Copy this template Repo.
2. Add 2 Repo Secrets called LEETCODE_CSRF_TOKEN and LEETCODE_SESSION from the leetcode-sync [documentation](https://github.com/joshcai/leetcode-sync?tab=readme-ov-file#how-to-use)
3. Edit the ```mkdocs.yml``` with your github and linkedin information (You can remove the socail section if you so wish).
4. Edit this README and Site_README.md with your website URL for the `Open App` badge and your leetcode account for the `leetcode stats card

*Optional (For Custom Domains)*

5. Edit the ```build-deploy-site.yml``` under the `Prepare docs folder` step uncomment the CNAME creation and add your url for example:
```yml
- name: Prepare docs folder
  run: |
    cp Style/overrides.css docs/
    echo "leetcode.romitsagu.com" > ./docs/CNAME # For custom domain if needed
    cp Site_README.md docs/README.md
```

**Note**
The table of Solutions is autmatically added to the end of the two READMEs if it doesn't already exist. Also the `README.md` is shown only on the GitHub and the `Site_README.md` is used for the website if you want to make different chanegs to them.


### Workflow Steps
1. Uses the ```joshcai/leetcode-sync``` GitHub action to will the problems and solutions from leetcode into the ```/Solutions``` folder.
2. Uses the Script ```update_project_readme.py``` to compile all of the completed problems into a table in 2 readme files that can be used for GitHub and the Mkdocs site
3. Uses the Script ```update_readmes.py.py``` to create README files from the problems and solutions and embed their difficulty, tags and the solution's statistics.
4. Uses Mkdocs to convert the READMEs created in `Step 3` to a website.
5. The website is then deployed using the GitHub Pages deploy action.

## My Leetcode Stats

<div align="center">
    <img src="https://leetcard.jacoblin.cool/NinePiece2?theme=dark" height="165" alt="leetcode stats"/>
</div>

## Table of my Solutions

