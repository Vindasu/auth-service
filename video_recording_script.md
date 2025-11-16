# CS 361 Sprint 2.6 Video Recording Script
## Auth Microservice Demonstration
**Target Duration: 8-10 minutes**
**Author: Alexander Adams, Group 64**

---

## 🎬 VIDEO STRUCTURE (Follow This Order)

### **INTRO (30 seconds)**
- "Hi, this is Alexander Adams from Group 64"
- "This is my CS 361 Sprint 2.6 microservice implementation" 
- "I'll be demonstrating my auth microservice with programmatic communication"
- "The video will show the test program, microservice responses, and README documentation"

---

### **PART 1: README DEMONSTRATION (3 minutes)**
**📋 Script:**
- "First, let me show you the README documentation"
- Open `README.md` in VS Code
- **SCROLL SLOWLY** through each section:

#### **Section 1: Communication Contract (45 seconds)**
- "Here's how other programs REQUEST data from my microservice"
- Pause at the code examples
- "Notice the clear API endpoints and request formats"
- "And here's how programs RECEIVE data back"
- Show the JSON response examples

#### **Section 2: API Endpoints Table (30 seconds)**
- "Here are all the available endpoints"
- Point out POST /auth/register/, POST /auth/login/, GET /auth/user/
- "Each endpoint is clearly documented with examples"

#### **Section 3: Communication Flow (30 seconds)**
- "This shows the simple 3-step communication sequence"
- Read the flow: "Register → Login → Get Profile"
- "Much cleaner than a complex UML diagram"

#### **Section 4: Setup Instructions (45 seconds)**
- "Complete setup instructions for anyone using this microservice"
- Scroll through prerequisites, installation, database setup
- "Everything needed to run the service"

#### **Section 5: Features & Security (30 seconds)**
- "Key features include dual login, JWT authentication, CORS support"
- "Built-in security features and SQLite database"

---

### **PART 2: MICROSERVICE DEMONSTRATION (4-5 minutes)**

#### **Step 1: Start the Microservice (30 seconds)**
**📋 Script:**
- "Now I'll demonstrate the actual microservice running"
- Open terminal, navigate to project folder
- "First, I activate the virtual environment"
- Run: `.\venv\Scripts\Activate.ps1`
- "Then start the Django microservice"
- Run: `python manage.py runserver`
- "The service is now running on localhost port 8000"

#### **Step 2: Show Test Program Code (1 minute)**
**📋 Script:**
- "Let me show you the test program that will make programmatic requests"
- Open `test_auth_service.py` in VS Code
- "This program demonstrates programmatic communication with the microservice"
- Scroll through the code slowly
- "It tests registration, login, and authenticated profile retrieval"
- "Notice how it sends JSON data and receives JSON responses"

#### **Step 3: Run Test Program - MAIN DEMO (2-3 minutes)**
**📋 Script:**
- Open a second terminal (keep Django running in first)
- "Now I'll run the test program to show live communication"
- Run: `python test_auth_service.py`

**As each test runs, narrate:**
- **Test 1 (Registration):**
  - "The test program sends a POST request to register a new user"
  - "The microservice receives the data, validates it, creates the user"
  - "It responds with status 201 and JWT tokens"
  - "This proves programmatic request and response communication"

- **Test 2 (Login):**
  - "Now it sends login credentials via POST request"  
  - "The microservice authenticates and returns JWT tokens"
  - "Notice the JSON response with user data"

- **Test 3 (Profile Retrieval):**
  - "Finally, an authenticated GET request using the JWT token"
  - "The microservice verifies the token and returns user profile"
  - "This shows secure, programmatic data exchange"

#### **Step 4: Verify Service Logs (30 seconds)**
- Switch back to Django terminal
- "You can see the microservice logged each request"
- Show the GET/POST requests in the Django output
- "This confirms the microservice received and processed each request"

---

### **PART 3: ADDITIONAL VERIFICATION (1-2 minutes)**

#### **Admin Panel (Optional - 1 minute)**
**📋 Script:**
- "Let me also show the Django admin panel as additional proof"
- Open browser to `http://127.0.0.1:8000/admin/`
- Login with admin credentials
- "Here you can see the user was actually created in the database"
- Show the Users table with the test361 user
- "This proves the microservice isn't just returning fake data"

#### **API Browser Test (Optional - 30 seconds)**
- Navigate to `http://127.0.0.1:8000/auth/user/` in browser
- "Without authentication, it correctly returns an error"
- "This shows the security is working properly"

---

### **CLOSING (30 seconds)**
**📋 Script:**
- "To summarize what we've demonstrated:"
- "✓ Complete README documentation with communication contract"
- "✓ Test program programmatically requesting data from microservice"
- "✓ Microservice programmatically responding with JSON data"
- "✓ Test program successfully receiving and displaying the responses"
- "✓ All communication is documented and working as specified"
- "This completes my CS 361 Sprint 2.6 microservice implementation"

---

## 🎯 RECORDING TIPS

### **Before Recording:**
- [ ] Close unnecessary browser tabs/applications
- [ ] Set screen resolution to 1920x1080 if possible
- [ ] Test audio levels
- [ ] Have both terminals ready
- [ ] Have VS Code and browser bookmarked

### **During Recording:**
- [ ] Speak clearly and at moderate pace
- [ ] Pause briefly between major sections
- [ ] Don't rush through README scrolling
- [ ] If you make a mistake, just continue (don't restart)
- [ ] Keep eye on time - aim for 8-9 minutes total

### **File Management:**
- [ ] Name video file: `CS361_Sprint2.6_AuthMicroservice_Group64_Adams.mp4`
- [ ] Keep video under 10 minutes total
- [ ] Test playback before submitting

---

## ⚠️ TROUBLESHOOTING

**If Django won't start:**
- Check virtual environment is activated
- Run `pip install -r requirements.txt`

**If test program fails:**
- Make sure Django is running first
- Check that `requests` is installed: `pip install requests`

**If registration fails:**
- User might already exist - that's fine, show the login working instead
- The program handles this gracefully

---

## 📋 RUBRIC CHECKLIST

- [ ] README shown and scrolled through slowly ✓
- [ ] Test program making programmatic requests ✓  
- [ ] Microservice responding with data ✓
- [ ] Test program receiving data back ✓
- [ ] All communication clearly demonstrated ✓
- [ ] Video under 10 minutes ✓
- [ ] Follows rubric order ✓

**Good luck with your recording! This script should help you create a professional, complete demonstration.**