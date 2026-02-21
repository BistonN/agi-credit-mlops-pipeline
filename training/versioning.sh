set -e

ART=/app/artifacts
MODELS=$ART/models
META=$ART/metadata.json

mkdir -p $MODELS

if [ -f $META ]; then
  LAST=$(jq -r '.current_version' $META | sed 's/v//')
else
  LAST=0
  echo '{"current_version":"v0","models":[]}' > $META
fi

NEW=v$((LAST+1))

mv $ART/model_v1.rds $MODELS/model_$NEW.rds

FEATURES=$(jq '.features' $ART/model_metadata.json)

jq \
  --arg ver "$NEW" \
  --arg time "$(date '+%Y-%m-%d %H:%M:%S')" \
  --argjson feats "$FEATURES" \
  '.models += [{"version":$ver,"created_at":$time,"features":$feats}]
   | .current_version=$ver' \
  $META > /tmp/meta.json

mv /tmp/meta.json $META

rm $ART/model_metadata.json

echo "Saved model $NEW"