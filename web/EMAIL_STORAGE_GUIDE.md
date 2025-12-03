# 사용자 이메일 저장 위치 가이드

## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다




## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다







## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다




## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다







## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다




## 📍 저장 위치

### 1. SQLite 데이터베이스 (주 저장소)
- **파일명**: `nexsupply_logs.db`
- **위치**: 프로젝트 루트 디렉토리
- **경로**: `C:\Users\kmyun\OneDrive\바탕 화면\nexsupply-platform\nexsupply_logs.db`

### 2. 저장되는 테이블

#### `consultation_requests` 테이블
상담 요청 시 저장되는 정보:
- `user_email` (필수) - 사용자 이메일 주소
- `user_name` - 사용자 이름 (선택)
- `product_query` - 제품/쿼리 정보
- `message` - 사용자 메시지
- `timestamp` - 요청 시간
- `status` - 상태 (기본값: 'pending')

#### `analysis_logs` 테이블
분석 리포트 요청 시 저장되는 정보:
- `user_email` (선택) - 리포트를 요청한 사용자 이메일
- `user_query` - 사용자 검색 쿼리
- `ai_result_json` - 전체 AI 분석 결과 (JSON)
- `timestamp` - 분석 시간

## 🔍 데이터 확인 방법

### 방법 1: Python으로 확인
```python
import sqlite3
import json

conn = sqlite3.connect('nexsupply_logs.db')
cursor = conn.cursor()

# 상담 요청 목록
cursor.execute("SELECT * FROM consultation_requests ORDER BY timestamp DESC LIMIT 10")
requests = cursor.fetchall()
for req in requests:
    print(req)

# 이메일 목록만 추출
cursor.execute("SELECT DISTINCT user_email FROM consultation_requests WHERE user_email IS NOT NULL")
emails = cursor.fetchall()
for email in emails:
    print(email[0])

conn.close()
```

### 방법 2: Streamlit Analytics Dashboard
- 앱 내부에 Analytics Dashboard 페이지가 있으면 거기서 확인 가능
- `services/data_logger.py`의 `render_analytics_dashboard()` 함수 사용

### 방법 3: SQLite 브라우저 사용
- DB Browser for SQLite (https://sqlitebrowser.org/) 설치
- `nexsupply_logs.db` 파일 열기

## 🔒 보안 주의사항

1. **GitHub에 업로드되지 않음**
   - `.gitignore`에 `*.db` 파일이 포함되어 있어 GitHub에는 업로드되지 않습니다
   - ✅ 안전합니다

2. **로컬 파일 보안**
   - 데이터베이스 파일은 로컬에만 저장됩니다
   - Streamlit Cloud 배포 시에는 클라우드 서버에 저장됩니다

3. **데이터 백업**
   - 정기적으로 `nexsupply_logs.db` 파일을 백업하세요
   - 민감한 정보(이메일 주소)가 포함되어 있습니다

## 📊 데이터 접근 함수

`services/data_logger.py`에 다음 함수들이 있습니다:

```python
# 최근 상담 요청 가져오기
get_consultation_requests(days=30, limit=100)

# 특정 이메일의 요청 내역
# (직접 SQL 쿼리 필요)
```

## 🚀 Streamlit Cloud 배포 시

- Streamlit Cloud에서는 자동으로 데이터베이스가 생성됩니다
- 파일은 Streamlit Cloud 서버에 저장됩니다
- 데이터는 Streamlit Cloud 계정과 연결된 저장소에 보관됩니다







