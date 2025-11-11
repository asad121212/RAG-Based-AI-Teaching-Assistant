"use client";

import { useState } from "react";

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async () => {
    const res = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setAnswer(data.answer || data.error);
  };

  return (
    <div className="min-h-screen bg-black text-cyan-300 p-10 flex flex-col items-center">
      <h1 className="text-4xl font-semibold mb-10">AI ASSISTANT TERMINAL</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask your question..."
        className="w-2/3 px-5 py-3 bg-transparent border border-cyan-400 rounded-lg
        outline-none focus:border-cyan-200 text-white"
      />

      <button
        onClick={ask}
        className="mt-6 px-10 py-3 bg-cyan-500 text-black rounded-lg 
        hover:bg-cyan-300 transition-all"
      >
        SEND
      </button>

      <div className="mt-10 w-2/3 bg-black border border-cyan-400 rounded-lg p-5">
        <p className="text-lg whitespace-pre-wrap">{answer}</p>
      </div>
    </div>
  );
}
