REGIONLIST=(`echo $(aws ec2 describe-regions --output text --query 'Regions[*].RegionName' | tr -s '\t' ' ')`)

for REGION in "${REGIONLIST[@]}"; do
    aws s3 cp "message_followers.zip" "s3://randhunt-code-${REGION}" --acl "public-read"
done
