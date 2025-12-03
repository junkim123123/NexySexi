# ⚡ NexSupply PWA 빠른 시작 가이드

**1주일 안에 Google Play Store 출시하기**

---

## 🚀 지금 바로 시작하기

### Step 1: Git 커밋 (2분)

```bash
git add .
git commit -m "feat: PWA 구현 완료 - Google Play Store 출시 준비"
git push
```

### Step 2: Streamlit Cloud 배포 (5분)

1. [Streamlit Cloud](https://share.streamlit.io) 접속
2. GitHub 저장소 연결
3. 배포 완료 후 `https://app.nexsupply.app` 접속 확인

### Step 3: PWA 검증 (5분)

1. Chrome에서 `https://app.nexsupply.app` 접속
2. F12 → Application → Manifest 확인
3. Service Worker 등록 확인

### Step 4: Bubblewrap 설치 (5분)

```bash
npm install -g @bubblewrap/cli
```

### Step 5: TWA 빌드 (30분)

**Windows:**
```powershell
.\build_twa.ps1
```

**Linux/Mac:**
```bash
chmod +x build_twa.sh
./build_twa.sh
```

### Step 6: assetlinks.json 배치 (10분)

```bash
# 빌드 후 생성된 파일 복사
cp nexsupply-twa/assetlinks.json .well-known/

# Git 커밋 및 푸시
git add .well-known/assetlinks.json
git commit -m "Add assetlinks.json for TWA"
git push
```

### Step 7: Google Play Console 등록 (1시간)

1. [Google Play Console](https://play.google.com/console) 접속
2. 앱 만들기
3. AAB 파일 업로드 (`nexsupply-twa/app-release-bundle.aab`)
4. 앱 정보 입력
5. 출시

---

## 📋 전체 가이드

- **상세 가이드**: `TWA_READ_ME.md`
- **빌드 가이드**: `BUILD_TWA.md`
- **Day 1 실행**: `DAY1_EXECUTION_GUIDE.md`

---

## ✅ 체크리스트

### 필수 파일
- [x] manifest.json
- [x] service-worker.js
- [x] streamlit_app.py (PWA 메타 태그 추가)
- [x] .streamlit/config.toml (enableStaticServing = true)

### 빌드 준비
- [ ] Node.js 설치
- [ ] Bubblewrap 설치
- [ ] 아이콘 파일 준비 (icon-192.png, icon-512.png)

### 배포
- [ ] Streamlit Cloud 배포
- [ ] assetlinks.json 배치
- [ ] Google Play Console 등록

---

**총 소요 시간: 약 2시간 + 심사 대기 (2-3일)**

🎉 **지금 바로 시작하세요!**




