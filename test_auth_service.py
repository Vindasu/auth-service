#!/usr/bin/env python3
"""
CS 361 Auth Service Test Program - Simple Version
Author: Alexander Adams, Group 64
"""

import requests
import json

# Test Auth Microservice
print("CS 361 Auth Service Test")
base_url = "http://127.0.0.1:8000"

# 1. Register user
print("\n1. Register new user")
user_data = {"username": "test_alex", "email": "test@coolio.com", "password": "Secure!", "password_confirm": "Secure!"}
response = requests.post(f"{base_url}/auth/register/", json=user_data)
print(f"   Request: POST {base_url}/auth/register/")
print(f"   Status Code: {response.status_code}")
if response.status_code == 201:
    data = response.json()
    print(f"   SUCCESS: User '{data['user']['username']}' created!")
    print(f"   Got JWT tokens: access={data['access'][:20]}...")
elif response.status_code == 400:
    print(f"   User already exists, continuing with login...")
else:
    print(f"   Error: {response.json()}")

# 2. Login 
print("\n2. Login with credentials")
login_data = {"login": "test_alex", "password": "Secure!"}
response = requests.post(f"{base_url}/auth/login/", json=login_data)
print(f"   Request: POST {base_url}/auth/login/")
print(f"   Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data['access']
    print(f"   SUCCESS: Login successful!")
    print(f"   User: {data['user']['username']} ({data['user']['email']})")
    print(f"   JWT Token: {token[:20]}...")
else:
    print(f"   Login failed: {response.json()}")
    token = None

# 3. Get user profile
print("\n3. Get user profile (authenticated request)")
if token:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/auth/user/", headers=headers)
    print(f"   Request: GET {base_url}/auth/user/")
    print(f"   Headers: Authorization: Bearer {token[:20]}...")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   SUCCESS: Got user profile!")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Date Joined: {user_data.get('date_joined', 'N/A')}")
    else:
        print(f"   Failed to get profile: {response.json()}")

print("\n" + "="*60)
print("MICROSERVICE TEST COMPLETE!")
print("Demonstrates programmatic API communication") 
print("Shows request/response data exchange")
print("Proves JWT authentication works")
print("="*60)