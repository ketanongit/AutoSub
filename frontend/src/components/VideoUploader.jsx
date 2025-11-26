import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileVideo, Loader2 } from 'lucide-react'
import axios from 'axios'

const VideoUploader = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    setUploading(true)
    setError(null)
    setProgress(0)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setProgress(percentCompleted)
        },
      })
      
      onUploadSuccess(response.data)
    } catch (err) {
      console.error(err)
      setError('Failed to upload video. Please try again.')
    } finally {
      setUploading(false)
    }
  }, [onUploadSuccess])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    },
    maxFiles: 1,
    multiple: false
  })

  return (
    <div className="max-w-xl mx-auto mt-20">
      <div 
        {...getRootProps()} 
        className={`
          border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300
          ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-600 hover:border-slate-400 hover:bg-slate-800/50'}
          ${uploading ? 'pointer-events-none opacity-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="p-4 bg-slate-800 rounded-full">
            {uploading ? (
              <Loader2 className="w-10 h-10 text-blue-400 animate-spin" />
            ) : (
              <Upload className="w-10 h-10 text-blue-400" />
            )}
          </div>
          
          <div className="space-y-2">
            <h3 className="text-xl font-semibold text-white">
              {uploading ? 'Uploading Video...' : 'Upload Video'}
            </h3>
            <p className="text-slate-400">
              {uploading 
                ? `${progress}% completed` 
                : 'Drag & drop a video file here, or click to select'
              }
            </p>
          </div>
          
          {!uploading && (
            <div className="flex items-center space-x-2 text-sm text-slate-500">
              <FileVideo className="w-4 h-4" />
              <span>Supports MP4, MOV, AVI, MKV</span>
            </div>
          )}
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-center">
          {error}
        </div>
      )}
    </div>
  )
}

export default VideoUploader
