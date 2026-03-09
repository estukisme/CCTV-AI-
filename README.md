# CCTV-AI Monitoring System

AI-based CCTV monitoring system for real-time object detection and anomaly detection.

## Features

- Real-time CCTV monitoring
- YOLO object detection
- CNN classification
- Snapshot logging system
- Alarm trigger system
- Monitoring dashboard

## System Architecture

Camera → RTSP Stream → AI Detection (YOLO/CNN) → Event Detection → Snapshot → Dashboard Monitoring

## Project Structure

CCTV-AI
│
├─ cnn/                # CNN training and model
├─ utils/              # Helper functions
├─ hybrid_GUI.py       # Main GUI application
├─ realtime_cctv.py    # CCTV stream processing
├─ predict.py          # Detection logic
├─ main_hybrid.py      # Main program
│
└─ snapshot_monitoring # Saved detection snapshots

## Installation

Clone repository
