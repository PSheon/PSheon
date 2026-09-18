<div align="center">
  <img src="./assets/images/welcome-banner.png" alt="See · Think · Act — computer vision · multi-agent · LLM · edge" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/PSheon">
    <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=600&size=22&duration=2600&pause=900&color=79DAFA&center=true&vCenter=true&width=760&lines=Machines+that+see%2C+agents+that+act;Multi-task+perception+on+the+edge+%E2%80%94+one+forward+pass;Multi-agent+orchestration+%C2%B7+LLM+%C2%B7+MCP;From+CCTV+frames+to+decisions%2C+in+metres" alt="typing intro" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/followers/PSheon?style=flat-square&color=79dafa&labelColor=0A0A23&label=followers" alt="followers" />
  <img src="https://komarev.com/ghpvc/?username=psheon&style=flat-square&color=ff6e96&label=visitors" alt="visitors" />
</p>

<img src="./assets/images/divider.svg" alt="" width="100%" />

## Hi there 👋

> 紙上得來終覺淺，絕知此事要躬行。
> <sub>What you read stays shallow; to truly know a thing, you have to build it.</sub>

I'm **Paul**. I build machines that see and agents that act, and I like to own the whole path: the perception model on the edge device, the tracks and events it produces, and the agents that decide what to do with them.

- 👁 **Computer vision** — multi-task perception networks, teacher / student distillation, ONNX / TensorRT on Jetson
- 🤝 **Multi-agent systems** — orchestrator / worker designs, MCP tool contracts, edge-and-cloud split
- 🧠 **LLM** — multimodal document understanding, structured output, VLMs on trigger rather than on every frame
- ⚡ **Edge** — RTSP ingest, GStreamer, WebRTC, Rust and Kotlin Multiplatform where Python is too slow
- 📍 Kaohsiung, Taiwan · building at [Syncrobotic](https://syncrobotic.ai/)

<img src="./assets/images/divider.svg" alt="" width="100%" />

## 🔭 What I'm building

### [HydraNet](https://github.com/Syncrobotic/SyncAI-Lib-HydraNet) — one camera, one model, everything in metres

<a href="https://github.com/Syncrobotic/SyncAI-Lib-HydraNet">
  <img src="https://raw.githubusercontent.com/Syncrobotic/SyncAI-Lib-HydraNet/main/assets/demo_Kaohsiung-cam04.gif" alt="HydraNet demo: detections and tracks on the left, the metric 3D scene with live dwell field on the right" width="100%" />
</a>

<sub>Left: person boxes and confirmed tracks, staff / customer verdict per person. Right: the same moment in metres, the store's fixtures reconstructed from one static plate, amber floor tiles are the live dwell field. Every face is blurred by the pipeline itself.</sub>

- **One ~8M-parameter network, one forward pass.** A shared RegNetX-800MF + BiFPN trunk carrying detection (`person`, `bag`, `device`, `boxed_stock`), pose (17 keypoints decoded inside the boxes) and terrain segmentation (`floor`, `wall`, `column`, `fixture`, `person`).
- **Teachers once, student every frame.** SAM 3, Grounding DINO, Depth-Anything V2 and ViTPose run once per camera to label and to fit the scene geometry. Anything constant on a fixed camera is cached, never learned. Only what changes frame to frame spends the GPU.
- **Tracks in metres, not pixels.** Boxes become floor positions through the cached geometry, so dwell, paths and queues come out in real units. Exported to ONNX / TensorRT for Jetson Orin, budgeted at 96 streams × 5 fps.

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧠 LLM</h3>
      <p><a href="https://github.com/PSheon/PDF2Markdown"><b>PDF2Markdown</b></a> — multimodal LLM transcription of PDFs and images into clean Markdown: tables, formulas and diagrams preserved. Gemini-powered, model-swappable.</p>
      <p>In HydraNet the VLM is a <i>trigger</i>, not a per-frame cost: rules and a tiny temporal model raise events, the VLM explains them.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🤝 Multi-Agent</h3>
      <p><b>Omnie agent orchestrator</b> — an orchestrator / worker design split across edge and cloud: perception workers stay on the device next to the camera, planning and retrieval run where the big models live, MCP defines the tool contract between them.</p>
      <p><sub>Private for now. Architecture notes coming.</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>👁 Computer Vision</h3>
      <p><a href="https://github.com/Syncrobotic/SyncAI-Lib-HydraNet"><b>HydraNet</b></a> — the multi-task perception network above, plus the commissioning pipeline (<code>syncai_bev3d</code>) that turns one static plate into a metric 3D scene, walkable floor, shelf ROIs and false-positive polygons per camera.</p>
    </td>
    <td width="50%" valign="top">
      <h3>⚡ Edge</h3>
      <p><a href="https://github.com/Syncrobotic/SyncAI-Data-RtspRecorder"><b>RtspRecorder</b></a> — multi-stream RTSP recording in Rust: auto-segment, reconnect, cross-day schedules, MKV → MP4, upload to GCS.</p>
      <p><a href="https://github.com/Syncrobotic/SyncAI-Lib-KmpWebRTC"><b>KmpWebRTC</b></a> — Kotlin Multiplatform WebRTC SDK with HTTP signaling and per-direction media control, zero WebRTC boilerplate.</p>
    </td>
  </tr>
</table>

<img src="./assets/images/divider.svg" alt="" width="100%" />

## 🧰 Stack

**Vision**

<p>
  <img src="https://img.shields.io/badge/PyTorch-0A0A23?style=for-the-badge&logo=pytorch&logoColor=79dafa" alt="PyTorch" />
  <img src="https://img.shields.io/badge/ONNX-0A0A23?style=for-the-badge&logo=onnx&logoColor=79dafa" alt="ONNX" />
  <img src="https://img.shields.io/badge/TensorRT%20%C2%B7%20Jetson-0A0A23?style=for-the-badge&logo=nvidia&logoColor=79dafa" alt="TensorRT / Jetson" />
  <img src="https://img.shields.io/badge/OpenCV-0A0A23?style=for-the-badge&logo=opencv&logoColor=79dafa" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Hugging%20Face-0A0A23?style=for-the-badge&logo=huggingface&logoColor=79dafa" alt="Hugging Face" />
  <img src="https://img.shields.io/badge/Python-0A0A23?style=for-the-badge&logo=python&logoColor=79dafa" alt="Python" />
</p>

**LLM / Agents**

<p>
  <img src="https://img.shields.io/badge/Claude-0A0A23?style=for-the-badge&logo=claude&logoColor=ff6e96" alt="Claude" />
  <img src="https://img.shields.io/badge/Gemini-0A0A23?style=for-the-badge&logo=googlegemini&logoColor=ff6e96" alt="Gemini" />
  <img src="https://img.shields.io/badge/Ollama-0A0A23?style=for-the-badge&logo=ollama&logoColor=ff6e96" alt="Ollama" />
  <img src="https://img.shields.io/badge/LangGraph-0A0A23?style=for-the-badge&logo=langgraph&logoColor=ff6e96" alt="LangGraph" />
  <img src="https://img.shields.io/badge/MCP-0A0A23?style=for-the-badge&logo=modelcontextprotocol&logoColor=ff6e96" alt="MCP" />
</p>

**Edge / Infra**

<p>
  <img src="https://img.shields.io/badge/ROS-0A0A23?style=for-the-badge&logo=ros&logoColor=b9a5ff" alt="ROS" />
  <img src="https://img.shields.io/badge/GStreamer-0A0A23?style=for-the-badge&logo=gstreamer&logoColor=b9a5ff" alt="GStreamer" />
  <img src="https://img.shields.io/badge/WebRTC-0A0A23?style=for-the-badge&logo=webrtc&logoColor=b9a5ff" alt="WebRTC" />
  <img src="https://img.shields.io/badge/Kotlin%20Multiplatform-0A0A23?style=for-the-badge&logo=kotlin&logoColor=b9a5ff" alt="Kotlin Multiplatform" />
  <img src="https://img.shields.io/badge/Rust-0A0A23?style=for-the-badge&logo=rust&logoColor=b9a5ff" alt="Rust" />
  <img src="https://img.shields.io/badge/Solidity-0A0A23?style=for-the-badge&logo=solidity&logoColor=b9a5ff" alt="Solidity" />
  <img src="https://img.shields.io/badge/Docker-0A0A23?style=for-the-badge&logo=docker&logoColor=b9a5ff" alt="Docker" />
  <img src="https://img.shields.io/badge/PostgreSQL-0A0A23?style=for-the-badge&logo=postgresql&logoColor=b9a5ff" alt="PostgreSQL" />
</p>

<sub>Also: TypeScript · React · Next.js. Ten years of frontend architecture is what the dashboards are built on.</sub>

<img src="./assets/images/divider.svg" alt="" width="100%" />

## 📈 Stats

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=psheon&layout=compact&theme=dracula&hide_border=true&langs_count=6&hide=html,css,arduino" />
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=psheon&layout=compact&title_color=ff6e96&icon_color=79dafa&hide_border=true&langs_count=6&hide=html,css,arduino" alt="PSheon | Top Languages" height="150px" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=psheon&theme=dracula&hide_border=true&show_icons=true&hide=contribs" />
    <img src="https://github-readme-stats.vercel.app/api?username=psheon&title_color=ff6e96&icon_color=79dafa&hide_border=true&show_icons=true&hide=contribs" alt="PSheon | GitHub Stats" height="150px" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=psheon&bg_color=282a36&color=f8f8f2&line=ff6e96&point=79dafa&area=true&hide_border=true" />
    <img src="https://github-readme-activity-graph.vercel.app/graph?username=psheon&bg_color=fffefe&color=434d58&line=ff6e96&point=79dafa&area=true&hide_border=true" alt="PSheon | Activity Graph" height="200px" />
  </picture>
</p>

<img src="./assets/images/divider.svg" alt="" width="100%" />

## 🤝 Find me

<p>
  <a href="https://psheon.buxx.finance"><img src="https://img.shields.io/badge/Blog-0A0A23?style=for-the-badge&logo=rss&logoColor=79dafa" alt="Blog" /></a>
  <a href="https://twitter.com/0xPSheon"><img src="https://img.shields.io/badge/X-0A0A23?style=for-the-badge&logo=x&logoColor=ffffff" alt="X / Twitter" /></a>
  <a href="https://www.linkedin.com/in/psheon/"><img src="https://img.shields.io/badge/LinkedIn-0A0A23?style=for-the-badge&logoColor=79dafa" alt="LinkedIn" /></a>
</p>
