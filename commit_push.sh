git config --local user.email "moohamadiann@gmail.com"
git config --local user.name "Mohsen"
git add .
git diff --quiet && git diff --staged --quiet || git commit -m "Add new songs"
git push