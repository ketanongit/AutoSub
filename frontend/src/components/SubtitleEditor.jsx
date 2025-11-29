import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Play, Pause, Download, Type, Palette, Layout, Wand2, Loader2 } from 'lucide-react'

const SubtitleEditor = ({ videoUrl, videoFilename, originalName }) => {
  const [subtitles, setSubtitles] = useState([])
  const [loading, setLoading] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [styles, setStyles] = useState({
    fontSize: 24,
    fontColor: '#ffffff',
    outlineColor: '#000000',
    outlineWidth: 2,
    marginV: 30,
    fontFamily: 'Arial'
  })
  
  const FONT_OPTIONS = [
    { name: 'Arial', value: 'Arial', type: 'system' },
    { name: 'Times New Roman', value: 'Times New Roman', type: 'system' },
    { name: 'Verdana', value: 'Verdana', type: 'system' },
    { name: 'Rubik', value: 'Rubik', type: 'google' },
    { name: 'Roboto', value: 'Roboto', type: 'google' },
    { name: 'Montserrat', value: 'Montserrat', type: 'google' },
    { name: 'Poppins', value: 'Poppins', type: 'google' },
    { name: 'Lato', value: 'Lato', type: 'google' },
  ]
  const [processing, setProcessing] = useState(false)
  
  const videoRef = useRef(null)

  const handleTranscribe = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/transcribe', {
        filename: videoFilename,
        model: 'base'
      })
      setSubtitles(response.data.segments)
    } catch (error) {
      console.error('Transcription failed:', error)
      alert('Transcription failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime)
    }
  }

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const getCurrentSubtitle = () => {
    return subtitles.find(sub => 
      currentTime >= sub.start && currentTime <= sub.end
    )
  }

  const handleExport = async () => {
    setProcessing(true)
    try {
      // Convert subtitles to SRT format
      let srtContent = ''
      subtitles.forEach((sub, index) => {
        const formatTime = (seconds) => {
          const date = new Date(0)
          date.setSeconds(seconds)
          const timeStr = date.toISOString().substr(11, 8)
          const ms = Math.floor((seconds % 1) * 1000).toString().padStart(3, '0')
          return `${timeStr},${ms}`
        }
        
        srtContent += `${index + 1}\n`
        srtContent += `${formatTime(sub.start)} --> ${formatTime(sub.end)}\n`
        srtContent += `${sub.text.trim()}\n\n`
      })

      const response = await axios.post('/api/burn', {
        video_filename: videoFilename,
        srt_content: srtContent,
        style_config: styles
      })

      // Download the file
      const link = document.createElement('a')
      link.href = `/outputs/${response.data.output_filename}`
      link.download = `subtitled_${originalName}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    } finally {
      setProcessing(false)
    }
  }

  const currentSub = getCurrentSubtitle()

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-[calc(100vh-120px)]">
      {/* Left Column: Video Preview */}
      <div className="lg:col-span-2 flex flex-col gap-4">
        <div className="relative bg-black rounded-xl overflow-hidden shadow-2xl aspect-video group">
          <video
            ref={videoRef}
            src={videoUrl}
            className="w-full h-full object-contain"
            onTimeUpdate={handleTimeUpdate}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            controls
          />
          
          {/* Subtitle Overlay */}
          <div 
            className="absolute left-0 right-0 text-center pointer-events-none transition-all duration-200"
            style={{ 
              bottom: `${styles.marginV}px`,
              padding: '0 20px'
            }}
          >
            {currentSub && (
              <span
                style={{
                  fontSize: `${styles.fontSize}px`,
                  color: styles.fontColor,
                  textShadow: `
                    -${styles.outlineWidth}px -${styles.outlineWidth}px 0 ${styles.outlineColor},
                    ${styles.outlineWidth}px -${styles.outlineWidth}px 0 ${styles.outlineColor},
                    -${styles.outlineWidth}px ${styles.outlineWidth}px 0 ${styles.outlineColor},
                    ${styles.outlineWidth}px ${styles.outlineWidth}px 0 ${styles.outlineColor}
                  `,
                  fontFamily: styles.fontFamily,
                  fontWeight: 'bold'
                }}
              >
                {currentSub.text}
              </span>
            )}
          </div>
        </div>

        {/* Playback Controls & Info */}
        <div className="bg-slate-800 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button 
              onClick={togglePlay}
              className="p-3 bg-blue-600 hover:bg-blue-500 rounded-full transition-colors"
            >
              {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
            </button>
            <div>
              <h3 className="font-medium text-white">{originalName}</h3>
              <p className="text-sm text-slate-400">
                {Math.floor(currentTime / 60)}:{Math.floor(currentTime % 60).toString().padStart(2, '0')}
              </p>
            </div>
          </div>
          
          {subtitles.length === 0 && !loading && (
            <button
              onClick={handleTranscribe}
              className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded-lg font-medium transition-colors"
            >
              <Wand2 className="w-4 h-4" />
              Auto-Generate Subtitles
            </button>
          )}

          {loading && (
            <div className="flex items-center gap-2 text-purple-400">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Transcribing audio...</span>
            </div>
          )}
        </div>
      </div>

      {/* Right Column: Controls & Editor */}
      <div className="bg-slate-800 rounded-xl flex flex-col overflow-hidden border border-slate-700">
        <div className="p-4 border-b border-slate-700 bg-slate-800/50">
          <h2 className="font-semibold text-lg flex items-center gap-2">
            <Layout className="w-5 h-5 text-blue-400" />
            Editor & Styles
          </h2>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {/* Style Controls */}
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Palette className="w-4 h-4" /> Style Settings
            </h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-xs text-slate-400">Font Family</label>
                <select 
                  value={styles.fontFamily}
                  onChange={(e) => setStyles({...styles, fontFamily: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none text-white"
                >
                  {FONT_OPTIONS.map(font => (
                    <option key={font.value} value={font.value} style={{ fontFamily: font.value }}>
                      {font.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs text-slate-400">Font Size</label>
                <input 
                  type="number" 
                  value={styles.fontSize}
                  onChange={(e) => setStyles({...styles, fontSize: parseInt(e.target.value)})}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs text-slate-400">Vertical Position</label>
                <input 
                  type="number" 
                  value={styles.marginV}
                  onChange={(e) => setStyles({...styles, marginV: parseInt(e.target.value)})}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs text-slate-400">Text Color</label>
                <div className="flex items-center gap-2">
                  <input 
                    type="color" 
                    value={styles.fontColor}
                    onChange={(e) => setStyles({...styles, fontColor: e.target.value})}
                    className="w-8 h-8 rounded cursor-pointer bg-transparent border-0 p-0"
                  />
                  <span className="text-xs font-mono text-slate-500">{styles.fontColor}</span>
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-xs text-slate-400">Outline Color</label>
                <div className="flex items-center gap-2">
                  <input 
                    type="color" 
                    value={styles.outlineColor}
                    onChange={(e) => setStyles({...styles, outlineColor: e.target.value})}
                    className="w-8 h-8 rounded cursor-pointer bg-transparent border-0 p-0"
                  />
                  <span className="text-xs font-mono text-slate-500">{styles.outlineColor}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="h-px bg-slate-700" />

          {/* Subtitle List */}
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Type className="w-4 h-4" /> Subtitles ({subtitles.length})
            </h3>
            
            <div className="space-y-2 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
              {subtitles.length === 0 ? (
                <div className="text-center py-8 text-slate-500 text-sm italic">
                  No subtitles yet. Click "Auto-Generate" to start.
                </div>
              ) : (
                subtitles.map((sub, index) => (
                  <div 
                    key={index}
                    className={`p-3 rounded-lg border transition-all ${
                      currentTime >= sub.start && currentTime <= sub.end
                        ? 'bg-blue-500/10 border-blue-500/50'
                        : 'bg-slate-900/50 border-slate-700 hover:border-slate-600'
                    }`}
                  >
                    <div className="flex justify-between text-xs text-slate-500 mb-1">
                      <span>{new Date(sub.start * 1000).toISOString().substr(14, 5)}</span>
                      <span>{new Date(sub.end * 1000).toISOString().substr(14, 5)}</span>
                    </div>
                    <textarea
                      value={sub.text}
                      onChange={(e) => {
                        const newSubs = [...subtitles]
                        newSubs[index].text = e.target.value
                        setSubtitles(newSubs)
                      }}
                      className="w-full bg-transparent border-none text-sm text-slate-200 focus:ring-0 p-0 resize-none"
                      rows={2}
                    />
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Export Button */}
        <div className="p-4 border-t border-slate-700 bg-slate-800">
          <button
            onClick={handleExport}
            disabled={subtitles.length === 0 || processing}
            className={`
              w-full flex items-center justify-center gap-2 py-3 rounded-lg font-bold text-white transition-all
              ${subtitles.length === 0 || processing
                ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-500 shadow-lg shadow-green-900/20'
              }
            `}
          >
            {processing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing Video...
              </>
            ) : (
              <>
                <Download className="w-5 h-5" />
                Export Video
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

export default SubtitleEditor
