import re

with open('app.py', 'r') as f:
    content = f.read()

# Replace all identity = get_jwt_identity() patterns with claims = get_jwt()
content = re.sub(r'identity = get_jwt_identity\(\)', 'claims = get_jwt()', content)

# Replace identity.get('role') with claims.get('role')
content = re.sub(r"identity\.get\('role'\)", "claims.get('role')", content)

# Replace identity['user_id'] with claims.get('user_id')
content = re.sub(r"identity\['user_id'\]", "claims.get('user_id')", content)

# Replace identity.get('role', 'student') with claims.get('role', 'student')
content = re.sub(r"identity\.get\('role', 'student'\)", "claims.get('role', 'student')", content)

with open('app.py', 'w') as f:
    f.write(content)

print('File updated successfully')
