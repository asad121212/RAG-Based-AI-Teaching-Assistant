"use client";

import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState("");

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.success) {
      setMsg("Uploaded: " + data.filename + " — Processing...");

      // AUTO-RUN PIPELINE
      const processRes = await fetch("/api/process", {
        method: "POST",
        body: JSON.stringify({ filename: data.filename }),
      });

      const processData = await processRes.json();

      if (processData.success) {
        setMsg("✅ Upload & Processing Complete!");
      } else {
        setMsg("❌ Processing Failed");
      }
    } else {
      setMsg("Upload failed");
    }
  };


  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black text-white relative overflow-hidden">

      {/* Background glow grid */}
      <div className="absolute inset-0 opacity-40 pointer-events-none">
        <div className="w-full h-full bg-[radial-gradient(circle_at_top,rgba(0,255,255,0.3),transparent)]"></div>
      </div>

      <h1 className="text-4xl mb-10 font-bold tracking-wide text-cyan-400">
        VIDEO UPLOAD TERMINAL
      </h1>

      {/* Cyberpunk File Box */}
      <label
        htmlFor="fileInput"
        className="w-80 h-44 border-2 border-cyan-400 rounded-xl
        flex flex-col justify-center items-center cursor-pointer
        hover:bg-cyan-500 hover:bg-opacity-20
        transition-all duration-300 relative
        shadow-[0_0_15px_rgba(0,255,255,0.6)]"
      >
        <div className="absolute inset-0 rounded-xl border border-cyan-300 blur-sm opacity-40"></div>

        <span className="text-cyan-300 text-lg mb-2">
          {file ? file.name : "Select file"}
        </span>
        <span className="text-xs text-cyan-200 opacity-80">
          Click to browse
        </span>
      </label>

      <input
        id="fileInput"
        type="file"
        accept="video/*"
        className="hidden"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      {/* Cyberpunk Upload Button */}
      <button
        onClick={uploadFile}
        className="mt-8 px-8 py-3 bg-cyan-500 text-black font-semibold tracking-wide rounded 
        hover:bg-cyan-300 hover:text-black transition-all duration-200
        shadow-[0_0_15px_rgba(0,255,255,0.7)] cursor-pointer"
      >
        Upload File
      </button>

      <p className="mt-6 text-cyan-300 text-lg">{msg}</p>
    </div>
  );
}
