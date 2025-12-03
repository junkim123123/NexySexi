# 상담 요청 확인 방법 가이드

## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장




## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장







## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장




## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장







## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장




## 🚀 빠른 확인 방법 (3가지)

### 방법 1: Python 스크립트 실행 (가장 빠름) ⭐

터미널에서 다음 명령어 실행:

```bash
python check_requests.py
```

**출력 예시:**
```
📊 총 5개의 상담 요청이 있습니다.

[1] 요청 ID: 1
    📧 이메일: user@example.com
    👤 이름: 홍길동
    📅 시간: 2025-01-15T10:30:00
    📦 제품/쿼리: USB 케이블 1000개 주문
    💬 메시지: 빠른 배송이 필요합니다
    ✅ 상태: pending
```

### 방법 2: Streamlit Analytics Dashboard (웹 UI) ⭐⭐

1. **Streamlit 앱 실행 중이어야 함**
2. 브라우저에서 다음 URL 접속:
   ```
   http://localhost:8590/analytics?admin=1
   ```
   
   또는 Streamlit Cloud 배포 시:
   ```
   https://your-app.streamlit.app/analytics?admin=1
   ```

3. **확인할 수 있는 정보:**
   - 📊 총 상담 요청 수
   - 📧 각 요청의 상세 정보 (이메일, 이름, 메시지)
   - 📈 통계 및 트렌드 분석
   - 🔍 인기 검색어
   - 📦 카테고리별 트렌드

### 방법 3: SQLite 브라우저 사용 (시각적 확인)

1. **DB Browser for SQLite 설치**
   - 다운로드: https://sqlitebrowser.org/
   
2. **데이터베이스 파일 열기**
   - 파일 위치: `nexsupply_logs.db` (프로젝트 루트)
   - 경로: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

3. **테이블 확인**
   - `consultation_requests` 테이블 클릭
   - 모든 상담 요청 데이터 확인 가능

## 📋 확인 가능한 정보

각 상담 요청에는 다음 정보가 포함됩니다:

- ✅ **이메일 주소** (필수)
- ✅ **사용자 이름** (선택)
- ✅ **제품/쿼리 정보**
- ✅ **사용자 메시지**
- ✅ **요청 시간** (타임스탬프)
- ✅ **상태** (pending, contacted, completed 등)

## 🔔 실시간 알림 받기

### 이메일 알림 (현재 구현됨)

상담 요청이 들어오면 자동으로 다음 이메일로 전송됩니다:
- **받는 사람**: `outreach@nexsupply.net`
- **제목**: `CONSULTATION REQUEST: [제품명] - [사용자 이메일]`
- **내용**: 사용자 정보 + 전체 분석 결과 JSON

### 데이터베이스 확인 (주 저장소)

이메일 전송이 실패해도 데이터베이스에는 항상 저장됩니다.

## 🛠️ 고급 사용법

### 특정 기간의 요청만 확인

Python 스크립트 수정:
```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE timestamp >= datetime('now', '-7 days')
    ORDER BY timestamp DESC
""")
```

### 특정 이메일의 요청만 확인

```python
cursor.execute("""
    SELECT * FROM consultation_requests
    WHERE user_email = ?
    ORDER BY timestamp DESC
""", ("user@example.com",))
```

### CSV로 내보내기

```python
import csv
import sqlite3

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultation_requests")

with open('requests.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

## 📍 파일 위치

- **데이터베이스 파일**: `nexsupply_logs.db` (프로젝트 루트)
- **확인 스크립트**: `check_requests.py` (프로젝트 루트)
- **Analytics 페이지**: `pages/analytics.py`

## ⚠️ 주의사항

1. **데이터베이스 파일은 Git에 업로드되지 않음**
   - `.gitignore`에 포함되어 있음
   - 로컬에만 저장됨

2. **Streamlit Cloud 배포 시**
   - 데이터베이스는 클라우드 서버에 저장됨
   - Analytics 페이지는 `?admin=1` 파라미터 필요

3. **보안**
   - Analytics 페이지는 인증 없이 접근 가능 (현재)
   - 프로덕션에서는 인증 추가 권장







