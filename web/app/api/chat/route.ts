import { NextRequest, NextResponse } from "next/server";
import { exec } from "child_process";
import path from "path";
import fs from "fs";

export async function POST(req: NextRequest) {
  try {
    const { query } = await req.json();

    const processedDir = path.join(process.cwd(), "public/processed");
    const pkl = fs.readdirSync(processedDir).find((f) =>
      f.endsWith("_embeddings.pkl")
    );

    if (!pkl)
      return NextResponse.json({
        success: false,
        error: "No embeddings found."
      });

    const embeddingsPath = path.join(processedDir, pkl);

    const script = path.join(
      process.cwd(),
      "python_pipeline",
      "chat_runner.py"
    );

    const py = `python "${script}" "${query}" "${embeddingsPath}"`;

    const chunksJson: any = await new Promise((resolve, reject) => {
      exec(py, (err, stdout, stderr) => {
        if (err) reject(stderr);
        else resolve(stdout);
      });
    });

    const parsed = JSON.parse(chunksJson);

    const context = parsed.chunks
      .map(
        (c: any) =>
          `Title: ${c.title}\nFrom ${c.start}s to ${c.end}s\nText: ${c.text}`
      )
      .join("\n\n");

    const finalPrompt = `
You are an AI teaching assistant.
ONLY answer using the context below.

${context}

--------------------
User: ${query}
`;

    // ask Ollama
    const response = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      body: JSON.stringify({
        model: "llama3.2",
        prompt: finalPrompt,
        stream: false,
      }),
      headers: { "Content-Type": "application/json" },
    });

    const ollamaData = await response.json();

    return NextResponse.json({
      success: true,
      answer: ollamaData.response,
    });
  } catch (err) {
    console.error(err);
    return NextResponse.json({
      success: false,
      error: "Chat failed.",
    });
  }
}
