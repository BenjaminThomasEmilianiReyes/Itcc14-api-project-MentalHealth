from app import app
import json


def run_full_flow():
    with app.app_context():
        client = app.test_client()

        # 1) Login as student
        s_login = client.post('/api/login', json={'username': 'demostudent', 'password': 'password123'})
        print('STUDENT LOGIN status:', s_login.status_code)
        s_json = s_login.get_json()
        print('STUDENT LOGIN json:', s_json)
        if s_login.status_code != 200 or 'token' not in s_json:
            print('Student login failed')
            return 1
        s_token = s_json['token']
        s_user_id = s_json.get('user_id')

        # 2) Student creates a mood
        mood_payload = {'user_id': s_user_id, 'mood': 'happy', 'mood_text': 'Test mood via script'}
        create_mood = client.post('/api/moods', json=mood_payload, headers={'Authorization': f'Bearer {s_token}'})
        print('CREATE MOOD status:', create_mood.status_code)
        print('CREATE MOOD json:', create_mood.get_json())
        if create_mood.status_code not in (200,201):
            print('Create mood failed')
            return 2

        # 3) Login as counselor
        c_login = client.post('/api/login', json={'username': 'democounselor', 'password': 'password123'})
        print('COUNSELOR LOGIN status:', c_login.status_code)
        c_json = c_login.get_json()
        print('COUNSELOR LOGIN json:', c_json)
        if c_login.status_code != 200 or 'token' not in c_json:
            print('Counselor login failed')
            return 3
        c_token = c_json['token']

        # 4) Counselor lists moods (should include student's mood)
        list_resp = client.get('/api/moods', headers={'Authorization': f'Bearer {c_token}'})
        print('COUNSELOR LIST MOODS status:', list_resp.status_code)
        list_json = list_resp.get_json()
        print('COUNSELOR LIST MOODS json:', list_json)
        if list_resp.status_code != 200:
            print('Listing moods failed')
            return 4

        # find the mood entry we added
        entry_id = None
        for item in list_json:
            if item.get('mood_text') == 'Test mood via script' and item.get('user_id') == s_user_id:
                entry_id = item.get('entry_id')
                break
        if not entry_id:
            print('Could not find created mood in counselor list')
            return 5

        # 5) Counselor approves the mood
        approve_resp = client.post(f'/api/moods/{entry_id}/approve', headers={'Authorization': f'Bearer {c_token}'})
        print('APPROVE status:', approve_resp.status_code)
        print('APPROVE json:', approve_resp.get_json())
        if approve_resp.status_code != 200:
            print('Approve failed')
            return 6

        # 6) Verify student can GET their moods and see approved=True
        s_list = client.get('/api/moods', headers={'Authorization': f'Bearer {s_token}'})
        print('STUDENT LIST status:', s_list.status_code)
        s_list_json = s_list.get_json()
        print('STUDENT LIST json:', s_list_json)
        found = False
        for it in s_list_json:
            if it.get('entry_id') == entry_id:
                print('Found approved field:', it.get('approved'))
                if it.get('approved'):
                    found = True
                break
        if not found:
            print('Approved flag not visible to student')
            return 7

        # 7) Student creates forum post
        forum_payload = {'content': 'Test forum post via script'}
        forum_resp = client.post('/api/forum', json=forum_payload, headers={'Authorization': f'Bearer {s_token}'})
        print('FORUM POST status:', forum_resp.status_code)
        forum_json = forum_resp.get_json()
        print('FORUM POST json:', forum_json)
        if forum_resp.status_code != 201:
            print('Forum post failed')
            return 8
        forum_id = forum_json.get('forum_id')

        # 8) Counselor replies to forum post
        reply_payload = {'content': 'Counselor reply from script'}
        reply_resp = client.post(f'/api/forum/{forum_id}/reply', json=reply_payload, headers={'Authorization': f'Bearer {c_token}'})
        print('REPLY status:', reply_resp.status_code)
        print('REPLY json:', reply_resp.get_json())
        if reply_resp.status_code != 201:
            print('Reply failed')
            return 9

        print('Full flow test completed successfully')
        return 0


if __name__ == '__main__':
    exit(run_full_flow())
