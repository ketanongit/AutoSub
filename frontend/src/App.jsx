import { useState } from 'react'
import VideoUploader from './components/VideoUploader'
import SubtitleEditor from './components/SubtitleEditor'

function App() {
  const [currentStep, setCurrentStep] = useState('upload') // upload, editor
  const [videoFile, setVideoFile] = useState(null)
  const [videoUrl, setVideoUrl] = useState(null)
  const [subtitles, setSubtitles] = useState([])

  const handleUploadSuccess = (fileInfo) => {
    setVideoFile(fileInfo)
    setVideoUrl(`/uploads/${fileInfo.filename}`)
    setCurrentStep('editor')
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <header className="bg-slate-800 border-b border-slate-700 p-4">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            AutoSub
          </h1>
        </div>
      </header>

      <main className="container mx-auto p-4 md:p-8">
        {currentStep === 'upload' && (
          <VideoUploader onUploadSuccess={handleUploadSuccess} />
        )}
        
        {currentStep === 'editor' && videoFile && (
          <SubtitleEditor 
            videoUrl={videoUrl} 
            videoFilename={videoFile.filename}
            originalName={videoFile.original_name}
          />
        )}
      </main>
    </div>
  )
}

export default App
