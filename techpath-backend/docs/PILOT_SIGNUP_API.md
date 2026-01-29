# Pilot Signup API Documentation

## Overview
Complete backend implementation for the pilot signup feature following TechPath's established patterns.

## API Endpoint

### Public Endpoint

#### POST `/api/v1/pilot-signup`
Submit a pilot application for business owners interested in the pilot program.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Rajesh Kumar",
  "email": "rajesh@gymfit.com",
  "phone": "+919876543210",
  "businessName": "GymFit Studio",
  "industry": "gym",
  "message": "We get 50+ WhatsApp inquiries daily and miss 60% of them."
}
```

**Request Fields:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | 2-100 chars, letters/spaces/hyphens only |
| email | string | Yes | Valid email format |
| phone | string | Yes | 10-15 chars, valid phone format |
| businessName | string | Yes | 2-100 chars, letters/spaces/hyphens only |
| industry | string | Yes | One of: travel, gym, retail, realestate, education, healthcare, other |
| message | string | No | 0-500 chars |

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "data": {
    "applicationId": "123",
    "submittedAt": "2025-01-29T10:30:00Z"
  }
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "name"],
      "msg": "Must contain only letters, spaces, and hyphens"
    }
  ]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Failed to submit application",
  "message": "Database error"
}
```

### Admin Endpoints (Authentication Required)

#### GET `/api/v1/pilot-signup/applications`
List all pilot signup applications with optional filtering.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 20, max: 100)
- `status` (string): Filter by status (new, contacted, qualified, rejected)
- `industry` (string): Filter by industry

**Response:**
```json
[
  {
    "id": 1,
    "name": "Rajesh Kumar",
    "email": "rajesh@gymfit.com",
    "phone": "+919876543210",
    "business_name": "GymFit Studio",
    "industry": "gym",
    "message": "We get 50+ WhatsApp inquiries daily...",
    "status": "new",
    "notes": null,
    "created_at": "2025-01-29T10:30:00",
    "updated_at": "2025-01-29T10:30:00"
  }
]
```

#### GET `/api/v1/pilot-signup/applications/{id}`
Get a single pilot signup application by ID.

**Response:** Same as list item above.

#### PUT `/api/v1/pilot-signup/applications/{id}`
Update pilot signup application status and notes.

**Request Body:**
```json
{
  "status": "contacted",
  "notes": "Called on 2025-01-29. Very interested, scheduled demo for Feb 5."
}
```

**Response:** Updated application object.

#### DELETE `/api/v1/pilot-signup/applications/{id}`
Delete a pilot signup application.

**Response:**
```json
{
  "success": true,
  "message": "Pilot signup application deleted successfully"
}
```

## Email Notification

When a pilot signup is submitted, an automated email is sent to:
- **Recipient:** `sanjeev@techpath.biz` (hardcoded)
- **Subject:** `New Pilot Application: {business_name} ({industry})`
- **Content:** Formatted HTML email with all application details

The email includes:
- Contact information (name, email, phone)
- Business information (business name, industry)
- Message (if provided)
- Link to view in admin panel

## Database Schema

**Table:** `pilot_signups`

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, INDEXED |
| phone | VARCHAR(50) | NOT NULL |
| business_name | VARCHAR(100) | NOT NULL |
| industry | VARCHAR(50) | NOT NULL, INDEXED |
| message | TEXT | NULL |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'new', INDEXED |
| notes | TEXT | NULL (admin notes) |
| ip_address | VARCHAR(50) | NULL |
| user_agent | VARCHAR(500) | NULL |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP, INDEXED |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

**Indexes:**
- `ix_pilot_signups_email` on email
- `ix_pilot_signups_status` on status
- `ix_pilot_signups_industry` on industry
- `ix_pilot_signups_created_at` on created_at

## Files Created

1. **Schema:** `app/schemas/pilot_signup.py`
   - PilotSignupCreate, PilotSignupUpdate, PilotSignupResponse, PilotSignupSubmitResponse

2. **Model:** `app/models/pilot_signup.py`
   - PilotSignup database model

3. **CRUD:** `app/crud/pilot_signup.py`
   - CRUDPilotSignup with methods for creating, filtering, and managing signups

4. **Endpoint:** `app/api/v1/endpoints/pilot_signup.py`
   - Public submission endpoint
   - Admin management endpoints

5. **Migration:** `app/db/migrations/versions/20250129_pilot_signups.py`
   - Database migration to create pilot_signups table

6. **Email Service:** Updated `app/services/email_service.py`
   - Added `send_pilot_signup_notification()` method

## Setup Instructions

### 1. Run Database Migration

```bash
cd techpath-backend

# Run the migration
alembic upgrade head
```

### 2. Verify Database Table

```sql
-- Check if table was created
SELECT * FROM pilot_signups LIMIT 1;

-- Verify indexes
SHOW INDEXES FROM pilot_signups;
```

### 3. Test the API

```bash
# Test public endpoint
curl -X POST http://localhost:8000/api/v1/pilot-signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+919876543210",
    "businessName": "Test Business",
    "industry": "retail",
    "message": "This is a test message"
  }'

# Test admin endpoint (requires authentication)
curl -X GET http://localhost:8000/api/v1/pilot-signup/applications \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing Checklist

- [ ] Database migration runs successfully
- [ ] Public endpoint accepts valid data
- [ ] Email notification sent to sanjeev@techpath.biz
- [ ] Validation rejects invalid data (email, phone, industry)
- [ ] Admin endpoints require authentication
- [ ] Status filtering works correctly
- [ ] Industry filtering works correctly
- [ ] Update and delete operations work
- [ ] IP address and user agent are captured

## Integration with Frontend

The frontend should send requests to `/api/v1/pilot-signup` with the required fields. Example using fetch:

```javascript
const response = await fetch('https://api.techpath.biz/api/v1/pilot-signup', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+919876543210',
    businessName: 'Example Corp',
    industry: 'retail',
    message: 'Looking to automate our inquiries'
  })
});

const data = await response.json();
if (data.success) {
  console.log('Application ID:', data.data.applicationId);
}
```

## Status Workflow

1. **new** - Initial status when application is submitted
2. **contacted** - Admin has reached out to the applicant
3. **qualified** - Applicant meets criteria for pilot program
4. **rejected** - Applicant doesn't meet criteria or declined

Admins can update status and add notes through the admin panel.

## Security Considerations

- Public endpoint has no rate limiting yet (consider adding)
- Email notification uses hardcoded recipient (secure)
- Admin endpoints require JWT authentication
- Input validation prevents SQL injection
- Phone and email formats are strictly validated
- IP address and user agent captured for fraud detection
