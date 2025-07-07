import { data, p } from 'motion/react-client';
import React, { useRef, useState } from 'react';


function App() {

  const fileInputRef = useRef(null);
  const [active, setActive] = useState(false)
  const [error, seterror] = useState('')
  const [fileName, setFileName] = useState('');
  const [regularization, setRegularization] = useState(0.01)
  const [rashomon_bound_multiplier, setRashomon_bound_multiplier] = useState(0.05)
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
      formData.append('regularization', regularization);
    formData.append('rashomon_bound_multiplier', rashomon_bound_multiplier);

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData
        })
        if (response.ok) {
          const result = await response.json()
          console.log('Backend response:', result)
          if (result.success) {
            // Send data to TimberTrek via postMessage
            const timbertrekIframe = document.getElementById('timbertrek-iframe')
            console.log('TimberTrek iframe:', timbertrekIframe)
            setActive(true)
            // Wait for iframe to load before sending data
            setTimeout(() => {
              const timbertrekIframe = document.getElementById('timbertrek-iframe')
              console.log('TimberTrek iframe after delay:', timbertrekIframe)
              if (timbertrekIframe) {
                console.log('Sending data to TimberTrek:', result.data)
                timbertrekIframe.contentWindow.postMessage({
                  type: 'TIMBERTREK_DATA',
                  data: result.data
                }, '*')
              } else {
                console.log('TimberTrek iframe not found after delay')
              }
            }, 2000) // Wait 2 seconds for iframe to load
          } else {
            seterror(result.error || 'Failed to process file')
          }
        } else {
          const errorData = await response.json()
          seterror(errorData.error || 'Upload failed')
        }

      } catch (error) {
        console.log('error while catching ', error);
        seterror('Network error occurred')
      }

    }
  };

  return (
    <>

      <div className="flex flex-col items-center justify-center min-h-screen bg-black gap-4 p-6">

        <h1 className='text-white text-5xl font-extrabold font-serif ' >TIMBER<span className='' >TREK</span></h1>

        <h1 className='text-white text-3xl' >uploade the file in csv formate </h1>
        <h2 className='text-white' >make sure csv file is preprocessed </h2>
        <div className="w-full max-w-md text-white space-y-4">
  <div>
    <label htmlFor="regularization" className="block  mb-1">Regularization (0.001 - 1): {regularization}</label>
    <input
      type="range"
      id="regularization"
      min="0.001"
      max="0.9"
      step="0.001"
      value={regularization}
      onChange={(e) => setRegularization(parseFloat(e.target.value))}
      className="w-full"
    />
  </div>
  <div>
    <label htmlFor="rashomon_bound_multiplier" className="block mb-1">Rashomon Multiplier (0.001 - 1): {rashomon_bound_multiplier}</label>
    <input
      type="range"
      id="rashomon_bound_multiplier"
      min="0.001"
      max="0.9"
      step="0.001"
      value={rashomon_bound_multiplier}
      onChange={(e) => setRashomon_bound_multiplier(parseFloat(e.target.value))}
      className="w-full"
    />
  </div>
</div>

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
        {active ? (<p className='text-white' >Processing complete! Visualization will appear below automatically.</p>) : (null)}
        {
          error && (<p className='text-sm text-gray-400' >
            {error}
          </p>)



        }

      </div>
      {active ? (<iframe
        id="timbertrek-iframe"
        src="http://localhost:3000"
        style={{ width: "100%", height: "90vh", border: "none" }}
        title="TimberTrek Visualization"
        onLoad={() => console.log('TimberTrek iframe loaded')}
      />) : (null)}

    </>


  );
}

export default App;
