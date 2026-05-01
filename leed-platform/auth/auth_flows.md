# Authentication & Authorization

## Authentication Methods

### 1. Email/Password (Primary)

**Flow:**
```
┌─────────┐         ┌─────────────┐         ┌──────────┐
│  User   │────────▶│  /login     │────────▶│  Verify  │
│         │         │             │         │  Password│
└─────────┘         └─────────────┘         └────┬─────┘
                                                  │
                         ┌────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Issue Tokens │
                  │ - Access     │
                  │ - Refresh    │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Return JWT   │
                  └──────────────┘
```

**Implementation:**
```python
# POST /auth/login
async def login(email: str, password: str) -> AuthResponse:
    # Find user
    user = await db.users.find_by_email(email)
    if not user:
        raise InvalidCredentials()
    
    # Verify password (bcrypt)
    if not bcrypt.verify(password, user.password_hash):
        raise InvalidCredentials()
    
    # Update last login
    await db.users.update_last_login(user.id)
    
    # Issue tokens
    access_token = jwt.encode({
        "sub": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY)
    
    refresh_token = jwt.encode({
        "sub": user.id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY)
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=86400,
        user=user
    )
```

### 2. Google OAuth (SSO)

**Flow:**
```
┌─────────┐         ┌─────────────┐         ┌──────────────┐
│  User   │────────▶│ Google Auth │────────▶│  Callback    │
│         │         │             │         │  /oauth/google│
└─────────┘         └─────────────┘         └──────┬───────┘
                                                    │
                           ┌────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Find/Create  │
                    │ User         │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Issue Tokens │
                    └──────────────┘
```

**Implementation:**
```python
# GET /auth/oauth/google
async def google_oauth():
    # Redirect to Google
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={CALLBACK_URL}&"
        f"scope=openid email profile&"
        f"response_type=code"
    )

# GET /auth/oauth/google/callback
async def google_callback(code: str):
    # Exchange code for tokens
    tokens = await exchange_code(code)
    
    # Get user info from Google
    google_user = await get_google_user(tokens["access_token"])
    
    # Find or create user
    user = await db.users.find_by_email(google_user.email)
    if not user:
        user = await db.users.create({
            "email": google_user.email,
            "name": google_user.name,
            "avatar_url": google_user.picture,
            "email_verified": True
        })
    
    # Issue tokens
    return issue_tokens(user)
```

### 3. Magic Link (Passwordless)

**Flow:**
```
┌─────────┐         ┌─────────────┐         ┌──────────────┐
│  User   │────────▶│ /magic-link │────────▶│  Send Email  │
│         │         │             │         │  with Token  │
└─────────┘         └─────────────┘         └──────────────┘
                                                    │
                           ┌────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ User clicks  │
                    │ link         │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Verify token │
                    │ Issue JWT    │
                    └──────────────┘
```

**Implementation:**
```python
# POST /auth/magic-link
async def send_magic_link(email: str):
    # Generate token
    token = secrets.token_urlsafe(32)
    
    # Store with expiration (15 minutes)
    await db.magic_tokens.create({
        "email": email,
        "token": hash(token),
        "expires_at": datetime.utcnow() + timedelta(minutes=15)
    })
    
    # Send email
    await email.send(
        to=email,
        subject="Login to LEED AI Platform",
        body=f"Click to login: https://app.leedai.io/auth/magic?token={token}"
    )

# GET /auth/magic
async def verify_magic_link(token: str):
    # Find token
    record = await db.magic_tokens.find_by_token(hash(token))
    if not record or record.expires_at < datetime.utcnow():
        raise InvalidToken()
    
    # Find or create user
    user = await db.users.find_by_email(record.email)
    if not user:
        user = await db.users.create({"email": record.email})
    
    # Delete used token
    await db.magic_tokens.delete(record.id)
    
    # Issue tokens
    return issue_tokens(user)
```

## Token Management

### Access Token
- **Type:** JWT
- **Lifetime:** 24 hours
- **Contains:** user_id, email, role
- **Usage:** API requests in Authorization header

### Refresh Token
- **Type:** JWT
- **Lifetime:** 30 days
- **Contains:** user_id, type="refresh"
- **Usage:** Get new access token

### Refresh Flow
```python
# POST /auth/refresh
async def refresh_token(refresh_token: str) -> AuthResponse:
    # Verify token
    payload = jwt.decode(refresh_token, SECRET_KEY)
    if payload.get("type") != "refresh":
        raise InvalidToken()
    
    # Find user
    user = await db.users.find_by_id(payload["sub"])
    if not user:
        raise InvalidToken()
    
    # Issue new tokens
    return issue_tokens(user)
```

## Authorization (RBAC)

### Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| `owner` | Organization owner | Full access |
| `admin` | Organization admin | Manage users, projects, billing |
| `consultant` | LEED consultant | Create projects, automate credits, review |
| `reviewer` | Can only review | Review assigned credits |
| `viewer` | Read-only access | View projects and status |

### Permissions Matrix

| Permission | Owner | Admin | Consultant | Reviewer | Viewer |
|------------|-------|-------|------------|----------|--------|
| Create project | ✅ | ✅ | ✅ | ❌ | ❌ |
| Edit project | ✅ | ✅ | ✅ | ❌ | ❌ |
| Delete project | ✅ | ✅ | ❌ | ❌ | ❌ |
| Automate credit | ✅ | ✅ | ✅ | ❌ | ❌ |
| Review credit | ✅ | ✅ | ✅ | ✅ | ❌ |
| View all projects | ✅ | ✅ | ✅ | ❌ | ❌ |
| View assigned projects | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage team | ✅ | ✅ | ❌ | ❌ | ❌ |
| Manage billing | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export data | ✅ | ✅ | ✅ | ❌ | ❌ |

### Permission Check Middleware

```python
async def require_permission(permission: str):
    async def checker(request: Request):
        user = request.state.user
        
        # Get user's role in organization
        membership = await db.organization_members.find(
            organization_id=request.state.org_id,
            user_id=user.id
        )
        
        # Check if role has permission
        role_permissions = {
            "owner": ["*"],
            "admin": ["project.*", "credit.*", "team.*", "billing.*"],
            "consultant": ["project.create", "project.edit", "credit.automate", "credit.review"],
            "reviewer": ["credit.review"],
            "viewer": ["project.view"]
        }
        
        permissions = role_permissions.get(membership.role, [])
        
        if "*" not in permissions and permission not in permissions:
            raise Forbidden()
        
        return user
    
    return checker

# Usage
@app.post("/projects")
async def create_project(
    data: CreateProjectRequest,
    user: User = Depends(require_permission("project.create"))
):
    ...
```

### Project-Level Permissions

```python
# Check if user can access specific project
async def can_access_project(user_id: str, project_id: str, permission: str) -> bool:
    # Check if user is project member
    member = await db.project_members.find(
        project_id=project_id,
        user_id=user_id
    )
    
    if not member:
        return False
    
    # Project-level roles
    project_permissions = {
        "manager": ["*"],
        "contributor": ["credit.automate", "credit.edit"],
        "reviewer": ["credit.review"],
        "viewer": ["project.view"]
    }
    
    permissions = project_permissions.get(member.role, [])
    return "*" in permissions or permission in permissions
```

## Session Management

### Web Sessions
- **Storage:** Redis
- **TTL:** 24 hours (matches access token)
- **Key:** `session:{user_id}:{session_id}`
- **Value:** {user_id, org_id, project_ids, permissions}

### API Sessions
- Stateless (JWT-based)
- No server-side storage
- Token validated on each request

### Logout
```python
# POST /auth/logout
async def logout(request: Request):
    # For web: clear session cookie
    response.delete_cookie("session")
    
    # For API: revoke refresh token
    refresh_token = request.headers.get("X-Refresh-Token")
    if refresh_token:
        await db.revoked_tokens.create({
            "token_hash": hash(refresh_token),
            "revoked_at": datetime.utcnow()
        })
    
    return {"message": "Logged out successfully"}
```

## Security Measures

### Password Requirements
- Minimum 8 characters
- At least one uppercase
- At least one lowercase
- At least one number
- At least one special character

### Rate Limiting
```python
# Login attempts
@rate_limit(max_requests=5, window=300)  # 5 attempts per 5 minutes
async def login(email: str, password: str):
    ...

# Magic link requests
@rate_limit(max_requests=3, window=3600)  # 3 per hour
async def send_magic_link(email: str):
    ...
```

### Password Reset
```python
# POST /auth/forgot-password
async def forgot_password(email: str):
    # Generate reset token
    token = secrets.token_urlsafe(32)
    
    # Store with expiration (1 hour)
    await db.password_resets.create({
        "email": email,
        "token": hash(token),
        "expires_at": datetime.utcnow() + timedelta(hours=1)
    })
    
    # Send email
    await email.send(
        to=email,
        subject="Reset your password",
        body=f"Reset link: https://app.leedai.io/auth/reset-password?token={token}"
    )

# POST /auth/reset-password
async def reset_password(token: str, new_password: str):
    # Verify token
    record = await db.password_resets.find_by_token(hash(token))
    if not record or record.expires_at < datetime.utcnow():
        raise InvalidToken()
    
    # Update password
    user = await db.users.find_by_email(record.email)
    await db.users.update_password(user.id, bcrypt.hash(new_password))
    
    # Delete used token
    await db.password_resets.delete(record.id)
    
    return {"message": "Password reset successfully"}
```

## Audit Logging

```python
async def log_auth_event(event_type: str, user_id: str, metadata: dict):
    await db.activity_log.create({
        "event_type": f"auth.{event_type}",
        "user_id": user_id,
        "metadata": metadata,
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "created_at": datetime.utcnow()
    })

# Log all auth events
- login.success
- login.failed
- logout
- password_reset.requested
- password_reset.completed
- magic_link.sent
- magic_link.used
- oauth.connected
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
