# 🚀 Deployment Information

## ✅ GitHub Repository
**URL:** https://github.com/JLPT4YOU/qwenai
**Status:** ✅ Pushed successfully

## 🔑 Environment Variables (For Vercel)

### 1. QWEN_TOKEN
**Get from:**
1. Go to https://chat.qwen.ai
2. Press F12 → Application → Cookies
3. Copy value of `token`

**Example:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3...
```

### 2. ADMIN_KEY
**Your key:**
```
3SW_mAZQLynHrIJpgioDu3OmZDHwFK_KDCaeHKu6nso
```
*(Đã lưu trong ADMIN_KEY.txt - không commit lên git)*

## 🚀 Deploy to Vercel

### Quick Steps:

1. **Go to:** https://vercel.com/new

2. **Import:** JLPT4YOU/qwenai

3. **Add Environment Variables:**
   - `QWEN_TOKEN` = (your token from browser)
   - `ADMIN_KEY` = `3SW_mAZQLynHrIJpgioDu3OmZDHwFK_KDCaeHKu6nso`

4. **Click Deploy**

### Or via CLI:
```bash
vercel
vercel env add QWEN_TOKEN production
vercel env add ADMIN_KEY production
vercel --prod
```

## ✅ After Deploy

### Test Your API:
```bash
# Health check
curl https://YOUR_PROJECT.vercel.app/health

# Test chat
curl -X POST https://YOUR_PROJECT.vercel.app/api/chat/quick \
  -H "Authorization: Bearer YOUR_QWEN_TOKEN" \
  -d '{"message": "Hello!"}'
```

### Update Token (When Expired):
```bash
curl -X POST https://YOUR_PROJECT.vercel.app/api/admin/token \
  -d '{
    "token": "NEW_TOKEN",
    "admin_key": "3SW_mAZQLynHrIJpgioDu3OmZDHwFK_KDCaeHKu6nso"
  }'
```

## 📚 Documentation

- **README.md** - Overview
- **QUICKSTART.md** - 5-minute setup
- **API_DOCS.md** - Complete API reference
- **DEPLOY.md** - Detailed deployment guide

---

**Ready to deploy!** 🎉
