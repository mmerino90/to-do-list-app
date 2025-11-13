# 🚨 DEPLOYMENT BLOCKED - Action Required

**Status**: ⏸️ CD Pipeline Halted - Awaiting GCP IAM Configuration  
**Issue**: Service account insufficient permissions  
**Error Code**: `artifactregistry.repositories.uploadArtifacts` denied  
**Commit**: `9a09f17` (documentation pushed)

---

## What Happened

✅ **CI Pipeline**: PASSED
- Tests ran successfully (10/10)
- Code coverage verified (81.75%)
- Docker image built

⏸️ **CD Pipeline**: BLOCKED AT PUSH STEP
- Trying to push image to Google Container Registry
- Service account permission denied
- Permission required: `artifactregistry.repositories.uploadArtifacts`

---

## What You Need To Do (Right Now)

### 1️⃣ Go to GCP Console
```
https://console.cloud.google.com/iam-admin/iam?project=github-actions-deployer-478018
```

### 2️⃣ Click "Grant Access"

### 3️⃣ Add Service Account Email
The email should be in your `GCP_SA_KEY` secret. Find it by looking for something like:
```
your-sa@github-actions-deployer-478018.iam.gserviceaccount.com
```

### 4️⃣ Add These 3 Roles (one at a time)
- ✅ **Artifact Registry Writer** (`roles/artifactregistry.writer`)
  - Allows pushing Docker images to GCR
  
- ✅ **Cloud Run Admin** (`roles/run.admin`)
  - Allows deploying to Cloud Run
  
- ✅ **Service Account User** (`roles/iam.serviceAccountUser`)
  - Allows using the service account

### 5️⃣ Click "Save"

### 6️⃣ Wait 2-3 Minutes
IAM permissions take time to propagate through Google's systems.

### 7️⃣ Re-run the Workflow
Go to: https://github.com/mmerino90/to-do-list-app/actions
- Click the failed "CD - Deploy to Google Cloud Run" workflow
- Click "Re-run failed jobs"
- Monitor the progress

---

## Why This Is Happening

When GitHub Actions runs the deployment workflow:

```
1. ✅ Build Docker image (local to runner)
2. ✅ Authenticate to GCP (using service account)
3. ✅ Configure Docker auth
4. ❌ TRY TO PUSH IMAGE
   → "Permission denied: artifactregistry.repositories.uploadArtifacts"
   → Service account doesn't have permission!
5. ⏸️ Workflow stops
```

The service account needs explicit IAM roles to perform these actions.

---

## After You Add the Permissions

The workflow will automatically:
1. ✅ Push Docker image to Google Container Registry
2. ✅ Deploy service to Cloud Run
3. ✅ Configure environment variables
4. ✅ Connect to Cloud SQL database
5. ✅ Run health checks
6. ✅ Display the service URL

Expected timeline: **8-10 minutes** from re-run to live service.

---

## Documentation Available

Created comprehensive guides (also in your repo):

1. **URGENT_GCP_IAM_FIX.md** (You are here)
   - Quick 5-minute fix steps
   - Copy-paste instructions

2. **GCP_IAM_SETUP.md**
   - Detailed IAM explanation
   - Via GCP Console steps
   - Via gcloud CLI steps
   - Verification methods
   - Troubleshooting

3. **Other helpful docs**:
   - TEST_DEPLOYMENT_REPORT.md
   - DEPLOYMENT_PIPELINE.md
   - WORKFLOW_FIXES.md

---

## Quick Links

| Resource | Link |
|----------|------|
| **GCP IAM Console** | https://console.cloud.google.com/iam-admin/iam?project=github-actions-deployer-478018 |
| **GitHub Actions** | https://github.com/mmerino90/to-do-list-app/actions |
| **GCP Service Accounts** | https://console.cloud.google.com/iam-admin/serviceaccounts?project=github-actions-deployer-478018 |
| **Cloud Run Console** | https://console.cloud.google.com/run/detail/us-central1/github-actions-deployer |
| **GCR Images** | https://console.cloud.google.com/gcr/images/github-actions-deployer-478018 |

---

## If You Get Stuck

### Permission still denied after adding roles?

- **Wait longer** - IAM can take 5-10 minutes to propagate
- **Check the email** - Verify you granted to the CORRECT service account
- **Verify role was added** - Go back to IAM page and confirm role shows up
- **Clear cache** - Try re-authenticating in GitHub Actions

### Can't find the service account email?

1. Look in your `GCP_SA_KEY` secret (search for `client_email`)
2. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
3. Look for an account with format: `name@github-actions-deployer-478018.iam.gserviceaccount.com`

### Which roles exactly?

```
MUST HAVE (all 3 required):
✓ roles/artifactregistry.writer
✓ roles/run.admin  
✓ roles/iam.serviceAccountUser

OPTIONAL (helpful):
• roles/storage.admin
• roles/logging.logWriter
```

---

## Timeline to Completion

```
NOW     → Add IAM roles in GCP Console (5 min)
+5 min  → Wait for permissions to propagate (2-3 min)
+8 min  → Re-run GitHub Actions workflow
+10 min → CI pipeline runs (2-3 min)
+13 min → CD pipeline runs (5-7 min)
         - Build image
         - Push to GCR (will now work!)
         - Deploy to Cloud Run
         - Health check
+20 min → ✅ SERVICE LIVE!
```

---

## What's Deployed

Once this is fixed:

**Application**: To-Do List API  
**Location**: Google Cloud Run (us-central1)  
**URL**: https://github-actions-deployer-570395440561.us-central1.run.app/  
**Database**: Cloud SQL PostgreSQL  
**CI/CD**: GitHub Actions  

**Available Endpoints**:
- `GET /api/v1/health` - Health check
- `GET /api/v1/ping` - Connectivity
- `GET /api/v1/metrics` - Prometheus metrics
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

---

## Next Steps

1. ✅ **NOW**: Go to GCP IAM Console (link above)
2. ✅ **NEXT**: Add 3 IAM roles to service account
3. ✅ **THEN**: Wait 2-3 minutes
4. ✅ **FINALLY**: Re-run the workflow

**Time to deploy**: ~30 minutes from now (5 min setup + 25 min pipeline)

---

**Status**: AWAITING YOUR ACTION  
**Priority**: HIGH (deployment is ready once IAM is configured)  
**See Also**: GCP_IAM_SETUP.md for detailed instructions
