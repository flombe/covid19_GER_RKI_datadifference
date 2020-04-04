#!/bin/sh

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout -b master
  git add bin/data_final.csv compare_plot.png
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER - Daily Data Update"
}

upload_files() {
  git remote add origin https://flombe:${GITHUB_AUTH_TOKEN}@github.com/flombe/covid19_GER_RKI_datadifference.git > /dev/null 2>&1
  git push --quiet --set-upstream origin master
}

echo "Setup Git..."
setup_git
echo "Add & Commit..."
commit_website_files
echo "Push..."
upload_files
echo "DONE.!"
