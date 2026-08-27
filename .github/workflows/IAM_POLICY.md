# IAM permissions for the deploy workflow

## What to create

One brand-new IAM user, dedicated to this repo's GitHub Actions
workflow. Do **not** reuse the shared Apex root/admin keys — one of the
reasons the 2026-08 revert incident was hard to diagnose was that the
same keys deployed everything, so it was impossible to tell which agent
or human touched S3 at what time. This user's activity in CloudTrail
should map 1:1 to `github.com/Kinggavint/hinderliter-hearing-proof`
pushes.

## Suggested user name

`hinderliter-github-deploy` (or whatever fits your Apex naming
convention).

## Access type

Programmatic access only (access key + secret). No console login. No
MFA (it's a machine identity).

## Attached policy (inline, single policy, exactly this)

Two statements. Nothing else. In particular, no `s3:*`, no `s3:Delete*`,
no CloudFront distribution updates, no ACM, no Lambda, no Route 53.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3WriteHinderliterBucketOnly",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::hinderliter-hearing-site",
        "arn:aws:s3:::hinderliter-hearing-site/*"
      ]
    },
    {
      "Sid": "CloudFrontInvalidateOneDistributionOnly",
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation",
        "cloudfront:GetInvalidation"
      ],
      "Resource": "arn:aws:cloudfront::*:distribution/E351Q8RD58U3KZ"
    }
  ]
}
```

## Why each permission is listed

- `s3:PutObject` — required to upload changed files during
  `aws s3 sync`.
- `s3:PutObjectAcl` — `aws s3 sync` may set object ACLs; harmless when
  bucket is private (typically ignored) but the API call still gets
  made, so denying it would fail the sync.
- `s3:GetObject` — `aws s3 sync` reads each object's ETag to decide
  whether to re-upload it.
- `s3:ListBucket` — `aws s3 sync` lists the bucket to compute the diff.
- `s3:GetBucketLocation` — the AWS SDK looks this up before any bucket
  operation.
- `cloudfront:CreateInvalidation` — invalidate `/*` after sync so users
  see the new content.
- `cloudfront:GetInvalidation` — `aws cloudfront wait invalidation-completed`
  polls this until the invalidation finishes.

## What this policy deliberately does NOT allow

- `s3:DeleteObject` — the workflow never deletes S3 objects. This is
  what protects the ~270 redirect objects from the 2026-07-16 soft-404
  fix from ever being nuked by a sync gone wrong.
- Any other S3 bucket — cannot touch platinum-partners, acihearing,
  kc-hearing, or any other Apex-owned bucket.
- Any other CloudFront distribution — cannot invalidate any other
  Apex-hosted site.
- CloudFront distribution updates (`UpdateDistribution`, etc.) — cannot
  change origins, cache behaviors, error responses, or attached
  certificates.
- Route 53, ACM, IAM, Lambda — none.

## After creating

Add the access key + secret as GitHub Actions secrets in the
`Kinggavint/hinderliter-hearing-proof` repo:

- Settings → Secrets and variables → Actions → New repository secret
- Name: `AWS_ACCESS_KEY_ID`, value: the access key ID
- Name: `AWS_SECRET_ACCESS_KEY`, value: the secret access key

Then trigger a test deploy by pushing any small commit to `main`, or
manually running the "Deploy to S3 + CloudFront" workflow from the
Actions tab.
