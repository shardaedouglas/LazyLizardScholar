# Demo Credentials for Parent Sign-In

## Test Account
To test the parent sign-in functionality, use these demo credentials:

**Email:** `demo@cyberstudy.com`  
**Password:** `demo123`

## Features Available
- **Sign In Page:** `/signin`
- **Parent Dashboard:** `/parent-dashboard` (requires authentication)
- **Session Management:** 30-day remember me option
- **Demo Data:** Sample student progress, projects, and achievements

## How to Test
1. Navigate to the sign-in page by clicking "Sign In" in the navigation
2. Enter the demo credentials above
3. Click "Sign In" to access the parent dashboard
4. Explore the dashboard features:
   - View student progress statistics
   - Check recent projects and achievements
   - See upcoming classes
   - Read messages from instructors

## Security Notes
- This is a demo account for testing purposes
- In production, passwords would be properly hashed and stored securely
- Session management includes proper authentication checks
- The system automatically creates this demo user on first startup

## Technical Details
- Authentication uses Flask sessions
- Passwords are hashed with SHA-256 and salt
- Session data is stored server-side
- Dashboard data is dynamically generated for demonstration
