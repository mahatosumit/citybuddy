# Auth-Gated App Testing Playbook (CityBuddy)

Do not be satisfied until auth-gated pages are tested completely.

## Step 1: Create Test User & Session (mongosh)
```
mongosh --eval "
use('test_database');
var userId = 'test-user-' + Date.now();
var sessionToken = 'test_session_' + Date.now();
db.users.insertOne({
  user_id: userId,
  email: 'test.user.' + Date.now() + '@example.com',
  name: 'Test User',
  picture: 'https://via.placeholder.com/150',
  role: 'admin',
  auth_provider: 'google',
  created_at: new Date()
});
db.user_sessions.insertOne({
  user_id: userId,
  session_token: sessionToken,
  expires_at: new Date(Date.now() + 7*24*60*60*1000),
  created_at: new Date()
});
print('Session token: ' + sessionToken);
print('User ID: ' + userId);
"
```

## Step 2: Test Backend API
```
curl -X GET "$URL/api/auth/me" -H "Authorization: Bearer YOUR_SESSION_TOKEN"
curl -X GET "$URL/api/favorites" -H "Authorization: Bearer YOUR_SESSION_TOKEN"
```

## Step 3: Browser Testing (set cookie)
```
await page.context.add_cookies([{
  "name": "session_token", "value": "YOUR_SESSION_TOKEN",
  "domain": "<host>", "path": "/", "httpOnly": True, "secure": True, "sameSite": "None"
}])
```
Also supported: email/password login via POST /api/auth/register and /api/auth/login (returns JWT used as Bearer token). A test account can be created this way for protected-flow testing.

## Checklist
- users doc has `user_id` (UUID), `role`; all queries use `{"_id":0}`.
- session.user_id matches users.user_id.
- /api/auth/me returns user (not 401); protected endpoints work with token.
- Public endpoints (places/weather/nepal/emergency/vision/trips-generate/chat-message) work WITHOUT token.

## Notes
- Google Auth (Emergent-managed) issues a `session_token` stored in `user_sessions` (7-day expiry), set as httpOnly cookie + usable as Bearer.
- Email/password issues a JWT (Bearer) — unified `current_user` accepts either.
