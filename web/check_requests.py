"""
NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()



NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()






NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()



NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()






NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()



NexSupply 상담 요청 확인 스크립트
간단하게 데이터베이스에서 상담 요청을 확인할 수 있습니다.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict

# 데이터베이스 경로
DB_PATH = os.path.join(os.path.dirname(__file__), "nexsupply_logs.db")


def get_consultation_requests(limit: int = 50) -> List[Dict]:
    """상담 요청 목록 가져오기"""
    if not os.path.exists(DB_PATH):
        print("❌ 데이터베이스 파일이 아직 생성되지 않았습니다.")
        print("   첫 사용자 요청이 들어오면 자동으로 생성됩니다.")
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, timestamp, user_email, user_name, 
                product_query, message, status
            FROM consultation_requests
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return []


def display_requests(requests: List[Dict]):
    """상담 요청을 보기 좋게 출력"""
    if not requests:
        print("\n📭 상담 요청이 없습니다.")
        return
    
    print(f"\n📊 총 {len(requests)}개의 상담 요청이 있습니다.\n")
    print("=" * 80)
    
    for i, req in enumerate(requests, 1):
        print(f"\n[{i}] 요청 ID: {req.get('id', 'N/A')}")
        print(f"    📧 이메일: {req.get('user_email', 'N/A')}")
        print(f"    👤 이름: {req.get('user_name', 'N/A') or '미입력'}")
        print(f"    📅 시간: {req.get('timestamp', 'N/A')}")
        print(f"    📦 제품/쿼리: {req.get('product_query', 'N/A')[:60]}")
        if req.get('message'):
            print(f"    💬 메시지: {req.get('message', '')[:100]}")
        print(f"    ✅ 상태: {req.get('status', 'pending')}")
        print("-" * 80)


def get_email_list(requests: List[Dict]) -> List[str]:
    """이메일 주소만 추출"""
    emails = []
    for req in requests:
        email = req.get('user_email')
        if email and email not in emails:
            emails.append(email)
    return emails


def main():
    """메인 함수"""
    print("=" * 80)
    print("🔍 NexSupply 상담 요청 확인")
    print("=" * 80)
    
    # 상담 요청 가져오기
    requests = get_consultation_requests(limit=50)
    
    # 요청 목록 출력
    display_requests(requests)
    
    # 이메일 목록 출력
    if requests:
        emails = get_email_list(requests)
        if emails:
            print(f"\n📧 총 {len(emails)}개의 고유 이메일 주소:")
            for email in emails:
                print(f"   • {email}")
    
    print("\n" + "=" * 80)
    print("💡 팁: Streamlit 앱에서 확인하려면")
    print("   http://localhost:8590/analytics?admin=1 로 접속하세요")
    print("=" * 80)


if __name__ == "__main__":
    main()







