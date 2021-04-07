function monaco_deploy(){
    monaco deploy --environments="config/dynatrace-environments.yaml" -p "nonprod" --continue-on-error=true
    return 0
}
monaco_deploy
echo "Exit code $?"