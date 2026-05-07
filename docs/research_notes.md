# Cognitive & Emotion-Aware AI: Core Concepts

This document explains the advanced concepts integrated into the Cognitive Mental Health Companion.

## 1. How Cognitive Computing is used
In this project, cognitive computing goes beyond simple pattern matching. It mimics human-like thought processes by:
- **Pattern Recognition**: Identifying long-term psychological trends instead of isolated moods.
- **Contextual Reasoning**: Using a memory system to understand *why* a user might be feeling a certain way based on past interactions.
- **Adaptive Learning**: Adjusting the bot's communication style (e.g., more supportive vs. more encouraging) based on the detected cognitive load.

## 2. Emotion-Aware AI Mechanics
We use a **Multi-Model Emotion Pipeline**:
- **Granular Classification**: Instead of just "Happy/Sad", we use the **GoEmotions** taxonomy (28 emotions) to detect subtle states like "remorse", "realization", or "anticipation".
- **Temporal Analysis**: Tracking how these emotions transition. A sudden shift from "joy" to "remorse" triggers a different safety protocol than a shift from "neutral" to "remorse".

## 3. Multimodal AI Integration
While the current version focuses on text, the architecture is designed for:
- **Acoustic Features**: Analyzing pitch, tone, and jitter from voice input to detect stress (VAD - Voice Activity Detection).
- **Visual Cues**: Facial landmark analysis to detect micro-expressions.
- **Integration Layer**: A "Late Fusion" approach where scores from text, audio, and video are weighted and combined into a single `EmotionalVector`.

## 4. Real-time Monitoring & Analytics
- **WebSocket Streaming**: As the user types, the backend calculates a "Per-Token Emotion" score.
- **Dashboard Synchronization**: The Chart.js frontend listens to a dedicated `/metrics` socket to update the "Stress Gauge" in real-time, providing immediate visual feedback on the conversation's health.

## 5. Model Evaluation
Performance is evaluated using:
- **F1-Score**: For emotion classification (crucial for imbalanced datasets).
- **Sentiment Accuracy**: Compared against human-annotated labels.
- **Safety Recall**: The most critical metric—ensuring 100% detection of "Crisis" keywords.
- **User Satisfaction (CSAT)**: Post-session feedback loops.
