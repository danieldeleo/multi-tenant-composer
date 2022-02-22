python3 -m pip install -r requirements.txt
apt-get install dnsutils -y

gcloud config set project "${PROJECT_ID}"

gcloud container clusters update "${GKE_CLUSTER}" \
  --enable-master-authorized-networks \
  --master-authorized-networks $(dig +short myip.opendns.com @resolver1.opendns.com)/32 --region "${REGION}"

gcloud container clusters get-credentials "${GKE_CLUSTER}" \
  --region "${REGION}" --project "${PROJECT_ID}"

KUB_SRVC_ACCT="${NAMESPACE}-service-acct"
GOOGLE_SRVC_ACCT="${GOOGLE_SRVC_ACCT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
kubectl create namespace "${NAMESPACE}"
kubectl create serviceaccount "${KUB_SRVC_ACCT}" --namespace "${NAMESPACE}"
kubectl annotate serviceaccount "${KUB_SRVC_ACCT}" --namespace "${NAMESPACE}" "iam.gke.io/gcp-service-account=${GOOGLE_SRVC_ACCT}"

gcloud iam service-accounts add-iam-policy-binding "${GOOGLE_SRVC_ACCT}" \
    --role roles/iam.workloadIdentityUser --member \
"serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KUB_SRVC_ACCT}]"


gsutil cp dags/* gs://us-east4-private-add25fff-bucket/dags