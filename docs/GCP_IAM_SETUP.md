# GCP IAM Permission Fix - Service Account Configuration

**Issue**: Service account lacks `artifactregistry.repositories.uploadArtifacts` permission

**Error**:
```
denied: Permission "artifactregistry.repositories.uploadArtifacts" denied on resource 
"projects/github-actions-deployer-478018/locations/us/repositories/gcr.io"
```

---

## Root Cause

The GitHub Actions service account does not have the required IAM roles to:
- Push Docker images to Google Container Registry (GCR)
- Push images to Artifact Registry
- Deploy to Cloud Run

---

## Solution

The service account needs the following IAM roles:

### Required IAM Roles

1. **Artifact Registry Writer** (for pushing images)
   - Role ID: `roles/artifactregistry.writer`
   - Permissions: Upload, download, and delete artifacts

2. **Cloud Run Admin** (for deploying services)
   - Role ID: `roles/run.admin`
   - Permissions: Create, update, delete Cloud Run services

3. **Service Account User** (for using service accounts)
   - Role ID: `roles/iam.serviceAccountUser`
   - Permissions: Act as a service account

4. **Storage Admin** (for GCS access, if needed)
   - Role ID: `roles/storage.admin`
   - Permissions: Full access to GCS

---

## How to Fix (GCP Console)

### Step 1: Go to Service Accounts
1. Open: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Select project: `github-actions-deployer-478018`
3. Find your service account used for GitHub Actions (likely named something like `github-actions-deployer` or similar)
4. Click on the service account email

### Step 2: Grant IAM Roles
1. In the service account details page, go to the **Members** or **Permissions** tab
2. Click **Grant Access**
3. Add these roles:
   - ✅ `roles/artifactregistry.writer`
   - ✅ `roles/run.admin`
   - ✅ `roles/iam.serviceAccountUser`
   - ✅ `roles/storage.admin` (optional, but helpful)

### Step 3: Save and Wait
1. Click **Save**
2. Wait 1-2 minutes for permissions to propagate
3. Re-run the GitHub Actions workflow

---

## How to Fix (gcloud CLI)

If you have the `gcloud` CLI installed locally:

```bash
# Set variables
export GCP_PROJECT_ID="github-actions-deployer-478018"
export SERVICE_ACCOUNT_EMAIL="[SERVICE_ACCOUNT_EMAIL]@iam.gserviceaccount.com"

# Grant required roles
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.admin"
```

Replace `[SERVICE_ACCOUNT_EMAIL]` with the actual service account email.

---

## How to Find Your Service Account Email

### Option 1: GCP Console
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Project: `github-actions-deployer-478018`
3. Look for a service account (email format: `name@github-actions-deployer-478018.iam.gserviceaccount.com`)
4. Copy the email address

### Option 2: Check GitHub Secrets
If you have access to the `GCP_SA_KEY` secret:
1. The service account email is inside the JSON file
2. Look for the `"client_email"` field

### Option 3: GCP Project IAM
1. Go to: https://console.cloud.google.com/iam-admin/iam
2. Project: `github-actions-deployer-478018`
3. Look for service accounts in the members list

---

## Verification

After granting permissions:

1. Wait 1-2 minutes for permissions to propagate
2. Go to: https://github.com/mmerino90/to-do-list-app/actions
3. Click **Run workflow** on the latest failed workflow
4. Select **CD - Deploy to Google Cloud Run** workflow (or re-trigger manually)
5. Monitor the workflow - the push step should now succeed

---

## Alternative: Update Workflow to Use gcloud

If you prefer not to change IAM permissions, you can modify the workflow to use `gcloud` commands instead of `docker push`:

```yaml
# Current approach (requires artifactregistry.writer)
- name: Push Docker image to Google Container Registry
  run: |
    docker push gcr.io/${{ env.GCP_PROJECT_ID }}/...

# Alternative approach (can use roles/run.admin only)
- name: Build and push with gcloud
  run: |
    gcloud builds submit --tag gcr.io/${{ env.GCP_PROJECT_ID }}/...
```

However, the IAM role fix is recommended as it's the standard approach.

---

## Complete IAM Setup Reference

### Minimal Required Roles (CD/Deployment Only)

```
✓ roles/artifactregistry.writer    # Push images to registry
✓ roles/run.admin                  # Deploy to Cloud Run
✓ roles/iam.serviceAccountUser     # Use service account
```

### Recommended Additional Roles

```
✓ roles/storage.admin              # For logs, artifacts in GCS
✓ roles/monitoring.metricWriter    # Write metrics (if needed)
✓ roles/logging.logWriter          # Write logs (if needed)
```

### Full Admin (Not Recommended for Security)

```
✗ roles/editor                     # Full project access (too permissive)
✗ roles/owner                      # Project owner (too permissive)
```

---

## Troubleshooting

### If permissions still denied after adding roles:

1. **Wait longer** - IAM changes can take 5-10 minutes to fully propagate
2. **Clear cache** - Try invalidating any cached credentials:
   ```bash
   gcloud auth application-default print-access-token
   ```
3. **Verify role grant** - Go back to IAM to confirm the role was actually added
4. **Check service account** - Ensure you granted to the correct service account

### If you see different errors:

- **"Cloud Run API not enabled"** → Enable Cloud Run API in GCP Console
- **"Cloud SQL instance not found"** → Verify Cloud SQL instance exists and is accessible
- **"Insufficient permission to create service"** → Ensure `roles/run.admin` is granted

---

## Testing the Fix

After updating IAM permissions:

1. **Immediate test** (if you have gcloud CLI):
   ```bash
   # Authenticate with the service account
   gcloud auth activate-service-account --key-file=path/to/key.json
   gcloud config set project github-actions-deployer-478018
   
   # Test artifact registry access
   gcloud artifacts repositories list
   ```

2. **Via GitHub Actions** (recommended):
   - Go to: https://github.com/mmerino90/to-do-list-app/actions
   - Click the failed workflow run
   - Click "Re-run failed jobs"
   - Watch the deployment progress

---

## Expected Success Indicators

After fixing IAM permissions, you should see:

```
✅ Build Docker image ........................ PASSED
✅ Push Docker image to GCR .................. PASSED
   - Image tagged with commit SHA
   - Image tagged as 'latest'
✅ Deploy to Cloud Run ........................ PASSED
   - Service deployed
   - Environment variables configured
   - Cloud SQL connection added
✅ Verify deployment .......................... PASSED
   - Health endpoint responds with 200
   - Returns {"status": "healthy"}
✅ Service URL ................................ DISPLAYED
   - https://github-actions-deployer-570395440561.us-central1.run.app/
```

---

## Quick Reference

| Task | Required Role | Notes |
|------|---------------|-------|
| Push to GCR | `artifactregistry.writer` | Essential |
| Deploy to Cloud Run | `run.admin` | Essential |
| Use service account | `iam.serviceAccountUser` | Essential |
| Access Cloud SQL | Included in `run.admin` | Usually included |
| Write logs | `logging.logWriter` | Optional |
| Write metrics | `monitoring.metricWriter` | Optional |

---

**Status**: Documentation complete - Ready for IAM configuration  
**Action Required**: Add IAM roles to service account in GCP Console  
**Estimated Fix Time**: 5-10 minutes (including propagation delay)
