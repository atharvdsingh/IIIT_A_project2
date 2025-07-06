# 🚀 TimberTrek Automatic Visualization Workflow

## 📋 Project Overview

This project creates an automated workflow where:
1. **User uploads CSV** → React frontend
2. **Backend processes** → Generates Rashomon set using TREEFARMS
3. **Data sent automatically** → TimberTrek visualization appears without manual steps

## 🏗️ Architecture

```
React Frontend (Port 5173) → Flask Backend (Port 5000) → TimberTrek (Port 3000)
     ↓                              ↓                        ↓
Upload CSV                    Process & Generate         Display Visualization
     ↓                              ↓                        ↓
Send to Backend              Return JSON Data         Receive via postMessage
     ↓                              ↓                        ↓
Receive JSON                 Send to TimberTrek        Show automatically
```

## 🔧 Changes Made

### 1. **Backend Changes (`backend/app.py`)**

#### **Modified `/upload` endpoint:**
- **Before:** Returned file download
- **After:** Returns JSON data directly
```python
# OLD: File download
return send_file(json_path, as_attachment=True)

# NEW: JSON response
return jsonify({
    'success': True,
    'data': decision_paths,
    'filename': f"decision_paths_{uuid.uuid4().hex[:8]}.json"
})
```

#### **Added backward compatibility:**
- New `/upload-file` endpoint for manual file downloads
- Original functionality preserved

### 2. **React Frontend Changes (`frontend/src/App.jsx`)**

#### **Modified file upload handler:**
```javascript
// OLD: Download file
const blob = await response.blob()
const downloadUrl = URL.createObjectURL(blob)
const a = document.createElement('a')
a.href = downloadUrl
a.download = 'decision_paths.json'
document.body.appendChild(a)
a.click()

// NEW: Process JSON and send to TimberTrek
const result = await response.json()
if (result.success) {
  const timbertrekIframe = document.getElementById('timbertrek-iframe')
  if (timbertrekIframe) {
    timbertrekIframe.contentWindow.postMessage({
      type: 'TIMBERTREK_DATA',
      data: result.data
    }, '*')
  }
  setActive(true)
}
```

#### **Updated iframe configuration:**
- Changed from public TimberTrek to local instance
- Added ID for postMessage communication
- Added onLoad handler for debugging

#### **Added debugging and timing:**
- Console logging for troubleshooting
- 2-second delay to ensure iframe loads
- Error handling improvements

### 3. **TimberTrek Changes (`timbertrek/src/components/timber/Timber.svelte`)**

#### **Added postMessage listener:**
```javascript
// Listen for postMessage from parent window (React frontend)
const handleMessage = (event: MessageEvent) => {
  if (event.data && event.data.type === 'TIMBERTREK_DATA') {
    console.log('Received data from React frontend:', event.data);
    initData(event.data.data);
  }
};

window.addEventListener('message', handleMessage);
```

### 4. **TimberTrek Default Dataset (`timbertrek/src/components/article/Article.svelte`)**

#### **Changed default selection:**
```javascript
// OLD: Default to 'compas'
let curDataset = 'compas';

// NEW: Default to 'my own set' for automatic data loading
let curDataset = 'my own set';
```

## 🚀 How to Run

### **Option 1: Use the startup script**
```bash
./start_services.sh
```

### **Option 2: Start manually**
```bash
# Terminal 1: Backend
cd backend
source tf-env/bin/activate
python app.py

# Terminal 2: TimberTrek
cd timbertrek
npm run dev

# Terminal 3: React Frontend
cd frontend
npm run dev
```

## 📊 Data Requirements

### **CSV Format:**
- **Target column:** Must be binary (0 and 1 only)
- **Last column:** Should be the target variable
- **Preprocessed:** Data should be ready for machine learning

### **Example CSV:**
```csv
feature1,feature2,feature3,target
1,2,3,1
2,3,4,0
3,4,5,1
```

## 🔍 Troubleshooting

### **Common Issues:**

1. **"Unexpected token '<'" Error:**
   - Check if backend is running on port 5000
   - Verify CORS is enabled
   - Check browser console for detailed errors

2. **Iframe not found:**
   - Ensure TimberTrek is running on port 3000
   - Check if iframe loads properly
   - Verify postMessage is being sent

3. **Model training errors:**
   - Ensure CSV has binary target (0/1)
   - Check data format and preprocessing
   - Verify sufficient data rows

### **Debug Steps:**
1. Open browser console (F12)
2. Upload CSV file
3. Check console messages:
   - `"Backend response: ..."`
   - `"TimberTrek iframe loaded"`
   - `"Sending data to TimberTrek: ..."`

## 🎯 Expected Workflow

1. **User visits:** `http://localhost:5173`
2. **Uploads CSV:** Clicks upload button, selects file
3. **Processing:** Backend generates Rashomon set
4. **Automatic visualization:** TimberTrek appears with data
5. **No manual steps:** Everything happens automatically

## 📁 File Structure

```
project/
├── backend/
│   ├── app.py                 # Modified Flask backend
│   ├── model/
│   │   └── backendModel.py    # TREEFARMS model
│   └── tf-env/               # Python virtual environment
├── frontend/
│   └── src/
│       └── App.jsx           # Modified React frontend
├── timbertrek/
│   └── src/
│       └── components/
│           ├── timber/
│           │   └── Timber.svelte    # Modified with postMessage
│           └── article/
│               └── Article.svelte   # Modified default dataset
├── start_services.sh         # Startup script
└── HELP.md                   # This file
```

## 🔧 Technical Details

### **Communication Flow:**
1. **React → Backend:** FormData with CSV file
2. **Backend → React:** JSON response with decision paths
3. **React → TimberTrek:** postMessage with data
4. **TimberTrek:** Receives data and displays visualization

### **Key Technologies:**
- **Backend:** Flask, TREEFARMS, pandas
- **Frontend:** React, Vite
- **Visualization:** TimberTrek (Svelte)
- **Communication:** postMessage API

### **Ports Used:**
- **Backend:** 5000
- **TimberTrek:** 3000
- **React Frontend:** 5173

## 🎉 Success Indicators

✅ **Backend:** Returns JSON with `success: true`  
✅ **Frontend:** Shows "Processing complete!" message  
✅ **TimberTrek:** Displays visualization automatically  
✅ **No manual steps:** User doesn't need to download/upload files  

## 🚀 Future Enhancements

- Add progress indicators during processing
- Support for different data formats
- Error recovery mechanisms
- Real-time updates during model training
- Support for multiple visualization types

---

**Created by:** AI Assistant  
**Date:** July 6, 2025  
**Purpose:** Automated CSV to TimberTrek visualization workflow 