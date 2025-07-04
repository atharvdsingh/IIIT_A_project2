import { data, p } from 'motion/react-client';
import React, { useRef, useState } from 'react';


function App() {
 
  const fileInputRef = useRef(null);
  const [active, setActive] = useState(false)

  const [error, seterror] = useState('')

  
  const [fileName, setFileName] = useState('');

  const handleFileChange = async (e) => {
    seterror('')
    const file = e.target.files[0]; 
    const fileName = file.name.toLowerCase();
    if (!fileName.endsWith(".csv")) {

      seterror('Only CSV files are allowed.')
      return;
    }
    if (file) {

      setFileName(file.name); 
      console.log("Selected file:", file.name);
      console.log(file)
      const formData = new FormData
      formData.append('file', file)

      try {
        const respons = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData
        })
        if (respons.ok) {
          const blob = await respons.blob()
          const downloadUrl = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = downloadUrl
          a.download = 'decision_paths.json'
          document.body.appendChild(a)
          a.click()
          a.remove()
          URL.revokeObjectURL(downloadUrl)
          setActive(true)
        }


      } catch (error) {
        console.log('error while cathcing ', error);


      }

    }
  };

  return (
    <>
    
    <div className="flex flex-col items-center justify-center min-h-screen bg-black gap-4 p-6">
     
      <h1 className='text-white text-5xl font-extrabold font-serif ' >TIMBER<span className='' >TREK</span></h1>

      <h1 className='text-white text-3xl' >uploade the file in csv formate </h1>
      <h2 className='text-white' >make sure csv file is preprocessed </h2>
      <button
        className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
        onClick={() => fileInputRef.current.click()} 
      >
        📁 Upload File
      </button>

      
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef}
        onChange={handleFileChange} 
        className="hidden"
      />

    
      {fileName && (
        <p className="text-sm text-gray-400">
          Selected: {fileName}
        </p>

      )}
      { active?( <p className='text-white' >scroll below and click <span className='text-red-700' >MY OWN SET</span>  and upload the <span className='text-red-700' >decision_paths.json</span>  file   </p> ):(null) }
      {
        error && (<p className='text-sm text-gray-400' >
          {error}
        </p>)



      }
      
    </div>
{active ? (<iframe
        src="https://poloclub.github.io/timbertrek"
        style={{ width: "100%", height: "90vh", border: "none" }}
        title="TimberTrek Visualization"
      />) : (null)}

</>


  );
}

export default App;
