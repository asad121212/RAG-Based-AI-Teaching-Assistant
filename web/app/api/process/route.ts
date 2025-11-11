import { NextRequest, NextResponse } from "next/server";
import { exec } from "child_process";
import path from "path";
import fs from "fs";

export async function POST(req: NextRequest) {
  try {
    // Read filename from request body
    const { filename } = await req.json();

    if (!filename) {
      return NextResponse.json({
        success: false,
        error: "Missing filename.",
      });
    }

    // Path to uploaded video
    const videoPath = path.join(process.cwd(), "public/uploads", filename);

    // Ensure processed directory exists
    const processedDir = path.join(process.cwd(), "public/processed");

    if (!fs.existsSync(processedDir)) {
      fs.mkdirSync(processedDir, { recursive: true });
    }

    // Path to pipeline script
    const pipelineScript = path.join(
      process.cwd(),
      "python_pipeline",
      "pipeline.py"
    );

    // Command to run Python pipeline
    const command = `python "${pipelineScript}" "${videoPath}" "${processedDir}"`;

    // Execute Python pipeline
    const output = await new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) reject(stderr);
        else resolve(stdout);
      });
    });

    return NextResponse.json({
      success: true,
      message: "Processing completed successfully",
      output,
    });
  } catch (err) {
    console.error("PROCESS ERROR:", err);
    return NextResponse.json({
      success: false,
      error: "Processing failed.",
    });
  }
}
