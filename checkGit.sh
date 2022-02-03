# Walk through all directories and run git status to 
# see where we are at.

for dir in */; do
    echo $"$dir"
    cd $dir
    git status
    cd ..
done
