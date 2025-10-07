# 🔑 Token Tips & Troubleshooting

## ✅ How to Copy Token Correctly

### Step-by-Step

1. **Go to chat.qwen.ai**
   - Open https://chat.qwen.ai
   - Make sure you're logged in

2. **Open Developer Tools**
   - Press `F12` (or `Cmd+Option+I` on Mac)
   - Go to **Application** tab

3. **Navigate to Local Storage**
   - Left sidebar → Local Storage
   - Click `https://chat.qwen.ai`

4. **Copy Token Value**
   - Find the row with key `token`
   - **Double-click** the value (right column)
   - Press `Cmd+A` (Mac) or `Ctrl+A` (Windows) to select all
   - Press `Cmd+C` (Mac) or `Ctrl+C` (Windows) to copy
   
   ⚠️ **Important**: Make sure you copy the **entire** value!

---

## ⚠️ Common Token Issues

### Issue 1: "String contains non ISO-8859-1 code point"

**Symptom:**
```
Error: Failed to read the 'headers' property from 'RequestInit': 
String contains non ISO-8859-1 code point
```

**Cause:** Token contains invisible characters (spaces, line breaks, special characters)

**Solutions:**

1. **Clear localStorage and re-enter token**
   ```javascript
   // In browser console (F12):
   localStorage.removeItem('qwen_token');
   location.reload();
   ```

2. **Copy token carefully**
   - Double-click the value in DevTools
   - Use Cmd+A / Ctrl+A to select all
   - Don't manually select with mouse (may miss parts)

3. **Paste into text editor first**
   - Paste token into Notepad/TextEdit
   - Remove any line breaks
   - Copy again from text editor
   - Paste into chat interface

---

### Issue 2: "Token không đúng định dạng JWT"

**Symptom:**
```
Token không đúng định dạng JWT!
Vui lòng đảm bảo:
- Copy toàn bộ token
- Không có khoảng trắng
- Không có ký tự đặc biệt
```

**Cause:** Token is incomplete or contains extra characters

**Valid JWT Format:**
```
eyJhbGciOi...AAA.eyJpZCI6I...BBB.1234567...CCC
       ↑              ↑             ↑
    Header         Payload      Signature
```

Must have **3 parts** separated by **2 dots** (`.`)

**Solution:**
- Make sure you copied the entire token
- Check there are exactly 2 dots
- No spaces at beginning or end
- Only contains: `A-Z`, `a-z`, `0-9`, `-`, `_`

---

### Issue 3: Token Expired

**Symptom:**
```
401 Unauthorized
Token expired
```

**Cause:** Token has passed its expiration time

**Check expiration:**
```javascript
// In browser console:
const token = localStorage.getItem('qwen_token');
const payload = JSON.parse(atob(token.split('.')[1]));
const expiresAt = new Date(payload.exp * 1000);
console.log('Expires:', expiresAt);
console.log('Now:', new Date());
```

**Solution:**
- Get a new token from chat.qwen.ai
- Or use the auto-refresh feature (built into the client)

---

### Issue 4: CORS Error

**Symptom:**
```
Access to fetch at 'https://chat.qwen.ai/api/...' blocked by CORS policy
```

**Cause:** Proxy server not running

**Solution:**
```bash
# Terminal 1: Start proxy
python proxy_server.py

# Terminal 2: Start web server
python3 -m http.server 8000

# Browser: Visit http://localhost:8000 (not file://)
```

---

## 🎯 Token Format Details

### JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4...
├─────────── Header ────────────┤├───────── Payload ─────────
                                 ↑
                           dot separator
```

**Valid characters:** `A-Z a-z 0-9 - _ .`

**Invalid characters:** 
- Spaces
- Line breaks
- Tabs
- Special characters (除了 `-` `_` `.`)
- Emojis or unicode

### Example Valid Token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjMzNjZ9.-S6huSievP_ddTRIPRoM0j8l2BN9ScEMZTgZnA9skik
```

### Example Invalid Tokens

❌ **Has line break:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4
LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRf...
```

❌ **Has spaces:**
```
eyJhbGciOiJI UzI1 NiIsInR5 cCI6I kpXVCJ9.eyJpZC I6Im...
```

❌ **Incomplete (missing parts):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6I...
                                        ↑ (only 1 dot, need 2)
```

---

## 🔧 Debug Commands

### Check if token is stored

```javascript
// In browser console (F12):
const token = localStorage.getItem('qwen_token');
console.log('Token exists:', !!token);
console.log('Token length:', token?.length);
console.log('First 50 chars:', token?.substring(0, 50));
```

### Check token format

```javascript
const token = localStorage.getItem('qwen_token');
const parts = token.split('.');
console.log('Token parts:', parts.length); // Should be 3
console.log('Header length:', parts[0]?.length);
console.log('Payload length:', parts[1]?.length);
console.log('Signature length:', parts[2]?.length);
```

### Decode token payload

```javascript
const token = localStorage.getItem('qwen_token');
try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log('User ID:', payload.id);
    console.log('Expires:', new Date(payload.exp * 1000));
    console.log('Issued:', new Date(payload.iat * 1000));
} catch (e) {
    console.error('Invalid token:', e);
}
```

### Clear token and restart

```javascript
localStorage.removeItem('qwen_token');
location.reload();
```

---

## 📋 Checklist: Before Reporting Issues

Before asking for help, check:

- [ ] Token copied from correct location (Local Storage → token)
- [ ] Token is complete (3 parts with 2 dots)
- [ ] No spaces or line breaks in token
- [ ] Proxy server is running (port 5001)
- [ ] Web server is running (port 8000)
- [ ] Visiting http://localhost:8000 (not file://)
- [ ] Token hasn't expired (check with decode command)
- [ ] Browser console shows no errors

---

## 💡 Pro Tips

### Tip 1: Use Incognito Window for Testing

Prevents conflicts with existing cookies/storage:
```
Cmd+Shift+N (Chrome)
Cmd+Shift+P (Firefox)
```

### Tip 2: Bookmark the Token Page

1. Get token from chat.qwen.ai
2. Save as bookmark for quick access
3. Update token whenever it expires

### Tip 3: Token Refresh is Automatic

The chat client automatically refreshes your token, so you rarely need to manually update it!

### Tip 4: Use Python CLI if Web has Issues

```bash
# Bypass all browser/CORS issues
export QWEN_TOKEN="your_token_here"
python chatbot.py
```

---

## 🔗 Related Docs

- `CORS_SOLUTION.md` - Fix CORS errors
- `TOKEN_REFRESH_GUIDE.md` - Auto-refresh tokens
- `RUN_WEB_CHAT.md` - Setup web chat
- `FINAL_SETUP.md` - Complete setup

---

**Last Updated**: 2025-10-07  
**Status**: ✅ Complete
