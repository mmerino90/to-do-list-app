# Immediate Action Required: Fix GCP Service Account Permissions

**Issue**: GitHub Actions deployment failing due to insufficient IAM permissions  
**Error**: `denied: Permission "artifactregistry.repositories.uploadArtifacts" denied`  
**Status**: ⏸️ DEPLOYMENT BLOCKED - Awaiting IAM Configuration

---

## Quick Fix (5 minutes)

### Step 1: Identify Your Service Account
The service account email is in the `GCP_SA_KEY` secret. If you have it locally:

```bash
# If you have the key file
cat path/to/key.json | grep "client_email"

# Output should look like:
# "client_email": "your-sa@github-actions-deployer-478018.iam.gserviceaccount.com"
```

Or go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=github-actions-deployer-478018

### Step 2: Grant Required Roles

**Via GCP Console** (easiest):
1. Go to: https://console.cloud.google.com/iam-admin/iam?project=github-actions-deployer-478018
2. Click **Grant Access**
3. Enter the service account email
4. Add roles:
   - `Artifact Registry Writer`
   - `Cloud Run Admin`
   - `Service Account User`
5. Click **Save**

**Via gcloud CLI** (if installed):
```bash
export SA_EMAIL="your-sa@github-actions-deployer-478018.iam.gserviceaccount.com"
export PROJECT="github-actions-deployer-478018"

gcloud projects add-iam-policy-binding $PROJECT \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/artifactregistry.writer

gcloud projects add-iam-policy-binding $PROJECT \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/run.admin

gcloud projects add-iam-policy-binding $PROJECT \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/iam.serviceAccountUser
```

### Step 3: Wait & Test
1. Wait 2-3 minutes for permissions to propagate
2. Go to: https://github.com/mmerino90/to-do-list-app/actions
3. Click the latest failed workflow
4. Click **Re-run failed jobs**
5. Monitor the deployment

---

## What's Needed

Your service account needs these 3 IAM roles:

| Role | Purpose | Current Status |
|------|---------|-----------------|
| `roles/artifactregistry.writer` | Push Docker images to GCR | ❌ MISSING |
| `roles/run.admin` | Deploy to Cloud Run | ❌ MISSING |
| `roles/iam.serviceAccountUser` | Use service account | ❌ MISSING |

---

## Exactly Where to Click (Step-by-Step)

### In GCP Console:

1. **Open IAM Console**
   ```
   https://console.cloud.google.com/iam-admin/iam?project=github-actions-deployer-478018
   ```

2. **Click "Grant Access"** button (top of the page)

3. **Enter Principal** (Service Account Email):
   ```
   your-service-account@github-actions-deployer-478018.iam.gserviceaccount.com
   ```

4. **Add Roles** (Click "Select a role", then search for each):
   - Search: "Artifact Registry Writer"
   - Search: "Cloud Run Admin"
   - Search: "Service Account User"

5. **Click "Save"**

6. **Confirm** in the popup

---

## Why This Error Occurred

```
denied: Permission "artifactregistry.repositories.uploadArtifacts"
```

**Translation**: Your service account doesn't have permission to push Docker images to Google Container Registry.

**Root Cause**: The service account was created but not granted the necessary IAM roles to interact with:
- Google Container Registry (for Docker images)
- Cloud Run (for deployment)
- IAM (for service account operations)

---

## After Adding Permissions

Once you've added the IAM roles:

1. **GitHub Actions** will be able to:
   - ✅ Build Docker images
   - ✅ Push images to Google Container Registry
   - ✅ Deploy to Cloud Run
   - ✅ Access Cloud SQL databases
   - ✅ Configure environment variables

2. **The workflow will**:
   - Complete successfully (no more permission errors)
   - Deploy the app to: https://github-actions-deployer-570395440561.us-central1.run.app/
   - Run health checks
   - Return the service URL

---

## Testing Locally (Optional)

If you want to verify the fix locally:

```bash
# Authenticate with the service account
gcloud auth activate-service-account --key-file=path/to/GCP_SA_KEY.json
gcloud config set project github-actions-deployer-478018

# Test artifact registry access
gcloud artifacts repositories list

# Test Cloud Run access
gcloud run services list --region=us-central1

# If both commands work, your IAM is fixed!
```

---

## Deployment Timeline (After Fix)

```
✓ You add IAM roles to service account
  ↓
⏱️ Wait 2-3 minutes (permissions propagate)
  ↓
🔄 Re-run failed GitHub Actions workflow
  ↓
📊 CI Pipeline runs (if not already done) → Takes 2-3 min
  ↓
🐳 Build Docker image → Takes 30 sec
  ↓
⬆️ Push to GCR → Takes 1-2 min (now with proper permissions!)
  ↓
☁️ Deploy to Cloud Run → Takes 1-2 min
  ↓
✅ Health check passes → Takes 10 sec
  ↓
🎉 App is live!
Total time: ~8-10 minutes from re-run
```

---

## Success Indicators

After the fix and re-run, you should see:

✅ GitHub Actions page shows **green checkmarks**  
✅ Docker image pushed to GCR (no "denied" errors)  
✅ Cloud Run service updated with new image  
✅ Health endpoint returns `200 OK` with `{"status": "healthy"}`  
✅ Workflow completion message shows service URL  

---

## Files to Reference

- **Full IAM Setup Guide**: See `GCP_IAM_SETUP.md`
- **Workflow File**: `.github/workflows/cd.yml`
- **Error Details**: Check GitHub Actions run logs

---

## Didn't Work?

If permissions still fail:

1. **Double-check the role names** - Use exact names from GCP console
2. **Verify you're in the right project** - `github-actions-deployer-478018`
3. **Wait longer** - IAM changes can take 5-10 minutes to fully propagate
4. **Check the service account email** - Make sure it's correct
5. **Look at GCP Activity Logs** - May show why permission was denied

---

**Next Step**: Add IAM roles to service account now, then re-run the workflow  
**Estimated Fix Time**: 5 minutes setup + 2-3 minutes permission propagation  
**Status After Fix**: Deployment will complete successfully 🚀

See `GCP_IAM_SETUP.md` for detailed instructions.
