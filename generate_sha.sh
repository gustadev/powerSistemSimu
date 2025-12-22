git stash && git checkout sha-tag
zip -r src.zip src -x '*__pycache__*'
shasum -a 512 src.zip
git switch -
rm src.zip