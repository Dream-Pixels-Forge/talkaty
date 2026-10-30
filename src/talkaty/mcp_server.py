"""talkaty MCP stdio server — exposes tts_generate, list_voices, list_personas, preview."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from .config import get_settings
from .pipeline import GenerateOptions, run
from .voices import list_personas, list_voices, resolve_persona


async def _call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "tts_generate":
        opts = GenerateOptions(
            script_path=args["script_path"],
            brief_path=args.get("brief_path"),
            voice=args.get("voice"),
            accent=args.get("accent"),
            backend=args.get("backend", "edge-tts"),
            pitch=float(args.get("pitch", 0.0)),
            speed=float(args.get("speed", 1.0)),
            output_path=args.get("output_path"),
            subtitles=args.get("subtitles", False),
        )
        result = await run(opts)
        return {
            "audio_path": result.path,
            "duration_seconds": result.duration_seconds,
            "voice_used": result.voice_used,
            "backend_used": result.backend_used,
        }

    if name == "list_voices":
        backend = args.get("backend", "edge-tts")
        voices = list_voices(backend)
        return {
            "voices": [
                {
                    "id": v.id,
                    "name": v.name,
                    "accent": v.accent,
                    "gender": v.gender,
                    "backend": v.backend,
                }
                for v in voices
            ]
        }

    if name == "list_personas":
        personas = list_personas()
        return {
            "personas": [
                {
                    "id": p.id,
                    "description": p.description,
                    "voice_id": p.voice_id("edge-tts"),
                    "accent": p.accent,
                    "gender": p.gender,
                    "backend": p.backend,
                }
                for p in personas
            ]
        }

    if name == "preview":
        text = args["text"]
        voice = args.get("voice", "smooth female")
        backend = args.get("backend", "edge-tts")
        persona = resolve_persona(voice, None, backend)
        import tempfile, os

        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(text)
            tmp = fh.name
        try:
            opts = GenerateOptions(script_path=tmp, voice=persona.id, backend=backend)
            result = await run(opts)
            return {"audio_path": result.path}
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    raise ValueError(f"Unknown tool: {name}")


async def _handle_message(message: dict[str, Any]) -> dict[str, Any]:
    method = message.get("method")
    params = message.get("params", {}) or {}
    msg_id = message.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "talkaty", "version": "0.1.0"},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "tts_generate",
                        "description": "Generate voiceover audio from script.md + brief",
                        "inputSchema": {
                            "type": "object",
                            "required": ["script_path"],
                            "properties": {
                                "script_path": {"type": "string"},
                                "brief_path": {"type": "string"},
                                "voice": {"type": "string", "default": "smooth female"},
                                "accent": {"type": "string", "default": "US"},
                                "backend": {"type": "string", "default": "edge-tts"},
                                "pitch": {"type": "number", "default": 0},
                                "speed": {"type": "number", "default": 1.0},
                                "output_path": {"type": "string"},
                                "subtitles": {"type": "boolean", "default": False},
                            },
                        },
                    },
                    {
                        "name": "list_voices",
                        "description": "List available TTS voices",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"backend": {"type": "string"}},
                        },
                    },
                    {
                        "name": "list_personas",
                        "description": "List voice personas",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                    {
                        "name": "preview",
                        "description": "Preview a short text sample with a voice",
                        "inputSchema": {
                            "type": "object",
                            "required": ["text"],
                            "properties": {
                                "text": {"type": "string"},
                                "voice": {"type": "string", "default": "smooth female"},
                                "backend": {"type": "string", "default": "edge-tts"},
                            },
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {}) or {}
        result = await _call_tool(tool_name, tool_args)
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"content": [{"type": "text", "text": str(result)}]},
        }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


async def _amain() -> None:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    writer = sys.stdout

    while True:
        line = await reader.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        import json

        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = await _handle_message(message)
        out = json.dumps(response) + "\n"
        writer.write(out)
        writer.flush()


def main() -> None:
    asyncio.run(_amain())


if __name__ == "__main__":
    main()
