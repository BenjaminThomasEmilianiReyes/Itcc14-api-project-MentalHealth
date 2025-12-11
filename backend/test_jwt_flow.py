from app import app

def run_test():
    with app.app_context():
        client = app.test_client()

        # Attempt login for seeded student
        login_resp = client.post('/api/login', json={'username': 'demostudent', 'password': 'password123'})
        print('LOGIN status:', login_resp.status_code)
        try:
            login_json = login_resp.get_json()
        except Exception:
            login_json = None
        print('LOGIN json:', login_json)

        if not login_json or 'token' not in login_json:
            print('Login failed, cannot continue test')
            return 2

        token = login_json['token']

        # Call protected endpoint
        moods_resp = client.get('/api/moods', headers={'Authorization': f'Bearer {token}'})
        print('MOODS GET status:', moods_resp.status_code)
        try:
            moods_json = moods_resp.get_json()
        except Exception:
            moods_json = None
        print('MOODS GET json:', moods_json)

        return 0

if __name__ == '__main__':
    exit(run_test())
